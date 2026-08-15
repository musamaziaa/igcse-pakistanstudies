"""Vercel serverless function: marks written exam answers with Claude.

Why this exists: the FastAPI backend runs on a free PythonAnywhere account,
whose outbound network is restricted to an allowlist that does not include
api.anthropic.com. Vercel functions have unrestricted egress, so the Anthropic
call lives here instead. ANTHROPIC_API_KEY is a Vercel environment variable and
never reaches the browser.

Flow:  browser -> POST /api/grade  -> Anthropic
       browser -> POST {backend}/exam/evaluate  (with the marks returned here)

This mirrors backend/utils/ai_grader.py. Keep SYSTEM_PROMPT and RESULT_SCHEMA
in sync with that file; run backend/scripts/sync_vercel_grader.py to refresh
the grading guides in ./grading_guides/.
"""

import json
import os
import time
from collections import deque
from http.server import BaseHTTPRequestHandler

import anthropic
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token

GRADER_MODEL = "claude-opus-5"
GRADER_EFFORT = "medium"
GUIDE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "grading_guides")
MAX_ITEMS = 40  # a single paper; also a cheap abuse guard

# This endpoint spends real money on every call, so it is not open to the
# internet: the caller must present a Google ID token we can verify, and each
# account gets a capped number of papers per hour.
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "")
RATE_LIMIT_PER_HOUR = int(os.environ.get("GRADE_RATE_LIMIT_PER_HOUR", "20"))
_RATE_WINDOW = 3600

_google_request = google_requests.Request()
# Per-instance only — Vercel may run several, so the real ceiling is
# RATE_LIMIT_PER_HOUR × instances. Enough to stop runaway usage; swap in Vercel
# KV or Upstash if you need an exact global limit.
_recent_calls: dict = {}


def verify_caller(auth_header: str) -> str:
    """Return the verified Google user id, or raise PermissionError."""
    if not GOOGLE_CLIENT_ID:
        raise PermissionError("GOOGLE_CLIENT_ID is not configured on the server.")
    scheme, _, token = (auth_header or "").partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise PermissionError("Sign in to have your answers marked.")
    try:
        claims = id_token.verify_oauth2_token(token, _google_request, GOOGLE_CLIENT_ID)
    except ValueError:
        raise PermissionError("Invalid or expired sign-in.")
    if claims.get("iss") not in ("accounts.google.com", "https://accounts.google.com"):
        raise PermissionError("Invalid token issuer.")
    sub = claims.get("sub")
    if not sub:
        raise PermissionError("Token has no subject.")
    return sub


def check_rate_limit(user_id: str) -> None:
    """Raise PermissionError if this user has graded too many papers recently."""
    now = time.time()
    calls = _recent_calls.setdefault(user_id, deque())
    while calls and now - calls[0] > _RATE_WINDOW:
        calls.popleft()
    if len(calls) >= RATE_LIMIT_PER_HOUR:
        raise PermissionError(
            f"Marking limit reached ({RATE_LIMIT_PER_HOUR} papers per hour). Try again later."
        )
    calls.append(now)

SYSTEM_PROMPT = """You are an experienced LRN International GCSE examiner marking a student's exam script.

Mark each answer against the mark scheme exactly as a real examiner would:

- Award marks for creditworthy content, not for matching the model answer word for word. A student who makes the same point in their own words earns the mark.
- Award partial credit. A 6-mark question that makes three of the required points earns 3, not 0.
- For extended and essay questions, mark by level of response: a developed, well-supported argument reaches the top band; a list of unexplained points sits in the lower band.
- A blank or entirely irrelevant answer earns 0.
- Never award more than the marks available for the question.
- Do not inflate marks to be kind. The score must be the one the student would receive in the real exam.

For each answer also write feedback the student can act on: what earned credit, what was missing, and what to add next time. Two or three sentences, addressed to the student as "you". Be specific about the content, not generic encouragement.

Where a marking guide for the subject is supplied below, it is the official standard: apply its level and band descriptors, command-word requirements and marking conventions in preference to your own judgement."""

RESULT_SCHEMA = {
    "type": "object",
    "properties": {
        "results": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "index": {"type": "integer", "description": "The index field of the question being marked."},
                    "marks_awarded": {"type": "integer", "description": "Marks awarded, from 0 to the question's marks available."},
                    "feedback": {"type": "string", "description": "Two or three sentences of specific, actionable feedback addressed to the student."},
                },
                "required": ["index", "marks_awarded", "feedback"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["results"],
    "additionalProperties": False,
}

_guide_cache = {}


def load_guide(subject: str) -> str:
    if subject not in _guide_cache:
        # Guard against path traversal in the subject name.
        safe = "".join(c for c in subject if c.isalnum() or c == "_")
        try:
            with open(os.path.join(GUIDE_DIR, f"{safe}.md"), encoding="utf-8") as fh:
                _guide_cache[subject] = fh.read().strip()
        except OSError:
            _guide_cache[subject] = ""
    return _guide_cache[subject]


def build_prompt(subject: str, items: list) -> str:
    lines = [f"Subject: {subject}", f"Mark the following {len(items)} written answers.", ""]
    for it in items:
        lines.append(f"--- QUESTION (index {it['index']}) ---")
        lines.append(f"Type: {it.get('type', 'written')}")
        lines.append(f"Marks available: {it['marks']}")
        if it.get("topic"):
            lines.append(f"Topic: {it['topic']}")
        lines.append(f"Question: {it.get('question', '')}")
        lines.append(f"Mark scheme / model answer: {it.get('model_answer') or '(none supplied)'}")
        student = (it.get("student_answer") or "").strip()
        lines.append(f"Student's answer: {student if student else '(left blank)'}")
        lines.append("")
    lines.append("Return one result per question, using the same index values shown above.")
    return "\n".join(lines)


def grade(subject: str, items: list) -> dict:
    """Returns {"results": {index: {marks_awarded, feedback}}} or raises RuntimeError."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY is not configured on the server.")

    client = anthropic.Anthropic(api_key=api_key)

    # Stable content first so the prefix caches; the breakpoint covers both blocks.
    system = [{"type": "text", "text": SYSTEM_PROMPT}]
    guide = load_guide(subject)
    if guide:
        system.append({
            "type": "text",
            "text": f"# Official marking guide for this subject\n\n{guide}",
            "cache_control": {"type": "ephemeral"},
        })
    else:
        system[0]["cache_control"] = {"type": "ephemeral"}

    response = client.messages.create(
        model=GRADER_MODEL,
        max_tokens=16000,
        system=system,
        output_config={
            "effort": GRADER_EFFORT,
            "format": {"type": "json_schema", "schema": RESULT_SCHEMA},
        },
        messages=[{"role": "user", "content": build_prompt(subject, items)}],
    )

    if response.stop_reason == "refusal":
        raise RuntimeError("The grading model declined to mark this submission.")

    text = next((b.text for b in response.content if b.type == "text"), "")
    payload = json.loads(text)

    by_marks = {it["index"]: it["marks"] for it in items}
    out = {}
    for row in payload.get("results", []):
        idx = row.get("index")
        if idx not in by_marks:
            continue
        # JSON Schema can't express numeric bounds, so clamp here.
        awarded = max(0, min(int(row.get("marks_awarded", 0)), by_marks[idx]))
        out[str(idx)] = {"marks_awarded": awarded, "feedback": (row.get("feedback") or "").strip()}
    return out


class handler(BaseHTTPRequestHandler):
    def _send(self, status: int, body: dict) -> None:
        payload = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_POST(self) -> None:
        try:
            user_id = verify_caller(self.headers.get("authorization", ""))
            check_rate_limit(user_id)
        except PermissionError as exc:
            return self._send(403, {"error": str(exc)})

        try:
            length = int(self.headers.get("content-length") or 0)
            if length > 1_000_000:
                return self._send(413, {"error": "Submission too large."})
            body = json.loads(self.rfile.read(length) or b"{}")
        except (ValueError, TypeError):
            return self._send(400, {"error": "Invalid JSON body."})

        subject = str(body.get("subject", "")).strip()
        items = body.get("items")
        if not subject or not isinstance(items, list):
            return self._send(400, {"error": "Expected {subject: str, items: [...]}."})
        if not items:
            return self._send(200, {"results": {}})
        if len(items) > MAX_ITEMS:
            return self._send(400, {"error": f"At most {MAX_ITEMS} questions per request."})

        try:
            for it in items:
                it["index"] = int(it["index"])
                it["marks"] = max(0, int(it.get("marks", 1)))
        except (KeyError, TypeError, ValueError):
            return self._send(400, {"error": "Each item needs an integer index and marks."})

        try:
            results = grade(subject, items)
        except Exception as exc:  # surfaced to the client as "not marked", not a crash
            return self._send(502, {"error": str(exc)})

        return self._send(200, {"results": results})

    def do_GET(self) -> None:
        self._send(200, {"status": "ok", "model": GRADER_MODEL,
                         "guides": sorted(f[:-3] for f in os.listdir(GUIDE_DIR) if f.endswith(".md"))})

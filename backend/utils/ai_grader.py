"""AI grading for written exam answers.

MCQs are graded by string comparison in main.py. Everything else (short_answer,
structured, extended, essay, fill_blank, case_study, evaluation,
logical_reasoning) has no machine-checkable answer, so it goes to Claude with
the question, the mark allocation and the model answer, and comes back with a
mark out of the allocation plus feedback.

All written questions in one submission are graded in a single request — one
API call per exam, not one per question.
"""

import json
import logging
import os

import anthropic
from dotenv import load_dotenv

# Load the repo-root .env explicitly: a bare load_dotenv() searches upward from
# the current working directory, which is not the repo root on PythonAnywhere.
load_dotenv(os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".env"
))

logger = logging.getLogger("nur-api")

# Grading is a well-scoped judgement task against a supplied mark scheme, so it
# runs at medium effort rather than the default high.
GRADER_MODEL = "claude-opus-5"
GRADER_EFFORT = "medium"

_client = None


class GradingUnavailable(Exception):
    """Raised when the grader cannot run (no key, API failure, refusal)."""


def _get_client():
    global _client
    if _client is None:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key or api_key == "your_key_here":
            raise GradingUnavailable(
                "ANTHROPIC_API_KEY is not set, so written answers cannot be graded."
            )
        _client = anthropic.AsyncAnthropic(api_key=api_key)
    return _client


DATA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data"
)

# Distilled from each subject's official spec, past papers and mark schemes by
# backend/scripts/build_grading_guides.py. Cached in-process: the file is read
# once per subject per server run, not once per exam.
_guide_cache: dict = {}


def load_grading_guide(subject: str) -> str:
    """Return the subject's marking guide, or "" if it hasn't been built."""
    if subject not in _guide_cache:
        path = os.path.join(DATA_DIR, subject, "grading_guide.md")
        try:
            with open(path, encoding="utf-8") as fh:
                _guide_cache[subject] = fh.read().strip()
        except OSError:
            logger.warning(
                "No grading_guide.md for %s — marking from the model answer alone. "
                "Run backend/scripts/build_grading_guides.py %s to build one.",
                subject, subject,
            )
            _guide_cache[subject] = ""
    return _guide_cache[subject]


SYSTEM_PROMPT = """You are an experienced LRN International GCSE examiner marking a student's exam script.

Mark each answer against the mark scheme exactly as a real examiner would:

- Award marks for creditworthy content, not for matching the model answer word for word. A student who makes the same point in their own words earns the mark.
- Award partial credit. A 6-mark question that makes three of the required points earns 3, not 0.
- For extended and essay questions, mark by level of response: a developed, well-supported argument reaches the top band; a list of unexplained points sits in the lower band.
- A blank or entirely irrelevant answer earns 0.
- Never award more than the marks available for the question.
- Do not inflate marks to be kind. The score must be the one the student would receive in the real exam.

Be forgiving about expression, strict about content. The real mark schemes require this — Pak Studies states "spelling and grammar must not be penalised", Islamiyat states "content takes precedence over language", Computer Science states "spelling and grammar should not be considered unless meaning is unclear":

- Never deduct marks for spelling, punctuation, grammar or capitalisation.
- Credit any spelling that is phonetically recognisable: "shahada"/"Shahadah", "Tarbella"/"Tarbela", "Kemal"/"Kamal", "Qibla"/"Qiblah". Only withhold the mark if the misspelling genuinely obscures the meaning or names something else entirely.
- Accept alternative transliterations and alternative names for the same thing (Salat / Salah / Namaz; Makkah / Mecca).
- Accept informal or second-language English. Many candidates are not writing in their first language. If the point is recognisable, award the mark.
- Never require the candidate's wording to match the model answer. Ask only whether the point was made.
- Do not withhold a mark because an answer is brief, so long as the required content is there.
- A minor slip that does not change the point being made — a date out by a year, a slightly imprecise figure — should not cost that mark unless the question is specifically testing that fact.
- Abbreviations and shorthand are fine where the meaning is clear.

You may mention spelling or expression in the feedback if it is worth improving, but it must not change the mark.

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
                    "index": {
                        "type": "integer",
                        "description": "The index field of the question being marked.",
                    },
                    "marks_awarded": {
                        "type": "integer",
                        "description": "Marks awarded, from 0 to the question's marks available.",
                    },
                    "feedback": {
                        "type": "string",
                        "description": "Two or three sentences of specific, actionable feedback addressed to the student.",
                    },
                },
                "required": ["index", "marks_awarded", "feedback"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["results"],
    "additionalProperties": False,
}


def _build_prompt(subject: str, items: list) -> str:
    lines = [
        f"Subject: {subject}",
        f"Mark the following {len(items)} written answers.",
        "",
    ]
    for it in items:
        lines.append(f"--- QUESTION (index {it['index']}) ---")
        lines.append(f"Type: {it['type']}")
        lines.append(f"Marks available: {it['marks']}")
        if it.get("topic"):
            lines.append(f"Topic: {it['topic']}")
        lines.append(f"Question: {it['question']}")
        lines.append(f"Model answer (an exemplar response, not the only acceptable one): {it['model_answer'] or '(none supplied)'}")
        if it.get("mark_scheme"):
            lines.append(f"Official mark scheme for this question: {it['mark_scheme']}")
        student = (it.get("student_answer") or "").strip()
        lines.append(f"Student's answer: {student if student else '(left blank)'}")
        lines.append("")
    lines.append(
        "Return one result per question, using the same index values shown above."
    )
    return "\n".join(lines)


async def grade_written_answers(subject: str, items: list) -> dict:
    """Grade written answers.

    `items` is a list of dicts with keys: index, question, type, marks,
    model_answer, student_answer, topic.

    Returns {index: {"marks_awarded": int, "feedback": str}}.
    Raises GradingUnavailable if the grader could not run.
    """
    if not items:
        return {}

    client = _get_client()

    # Stable content first so the prefix caches: the global instructions never
    # change, and the subject's guide changes only when the guides are rebuilt.
    # The breakpoint on the last block caches both.
    system = [{"type": "text", "text": SYSTEM_PROMPT}]
    guide = load_grading_guide(subject)
    if guide:
        system.append({
            "type": "text",
            "text": f"# Official marking guide for this subject\n\n{guide}",
            "cache_control": {"type": "ephemeral"},
        })
    else:
        system[0]["cache_control"] = {"type": "ephemeral"}

    try:
        response = await client.messages.create(
            model=GRADER_MODEL,
            max_tokens=16000,
            system=system,
            output_config={
                "effort": GRADER_EFFORT,
                "format": {"type": "json_schema", "schema": RESULT_SCHEMA},
            },
            messages=[{"role": "user", "content": _build_prompt(subject, items)}],
        )
    except anthropic.APIError as exc:
        logger.error("AI grading request failed: %s", exc)
        raise GradingUnavailable(f"Grading service error: {exc}") from exc

    if response.stop_reason == "refusal":
        logger.error("AI grading refused: %s", response.stop_details)
        raise GradingUnavailable("The grading model declined to mark this submission.")

    text = next((b.text for b in response.content if b.type == "text"), "")
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        logger.error("AI grading returned unparseable output: %s", text[:500])
        raise GradingUnavailable("Grading service returned an unreadable response.") from exc

    by_marks = {it["index"]: it["marks"] for it in items}
    graded = {}
    for row in payload.get("results", []):
        idx = row.get("index")
        if idx not in by_marks:
            continue
        # Clamp: JSON Schema cannot express numeric bounds, so enforce here.
        awarded = max(0, min(int(row.get("marks_awarded", 0)), by_marks[idx]))
        graded[idx] = {
            "marks_awarded": awarded,
            "feedback": row.get("feedback", "").strip(),
        }

    missing = set(by_marks) - set(graded)
    if missing:
        logger.warning("AI grading returned no result for question indexes %s", sorted(missing))

    return graded

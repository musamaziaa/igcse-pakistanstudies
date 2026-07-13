import sys
import os
import json
import random
import time
import logging
import uuid
from datetime import datetime, date, timedelta
from typing import List, Dict, Any, Optional

# --- Robust Path Setup ---
# This ensures that 'tasks' and 'utils' can be imported regardless of where the script is run from.
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("nur-api")

app = FastAPI(title="Nur Academy API", description="Backend for IGCSE Islamiyat Prep")

# Configure CORS
origins = ["*"] # Allow all for local development debugging

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = os.path.join(CURRENT_DIR, "data")
STUDENTS_DIR = os.path.join(DATA_DIR, "students")

# ── Models ───────────────────────────────────────────────────────────────────

class ExamSetup(BaseModel):
    student_name: str
    inc_quran: bool = True
    inc_hadith: bool = True
    inc_b: bool = True
    inc_c: bool = True
    mode: str = "Mixed (MCQ + Extended)"
    n_questions: int = 10

class MemorizeAttempt(BaseModel):
    groups_selected: List[str]
    cards_completed: int
    cards_total: int

class ExamSubmission(BaseModel):
    student_name: str
    questions: List[Dict[str, Any]]
    answers: Dict[str, str] # Note: JSON keys are strings
    time_taken: int

# ── Per-User Progress Models ─────────────────────────────────────────────────

import urllib.request
import urllib.parse
import threading

class UserProfile(BaseModel):
    name: str
    email: str
    picture: str = ""
    whatsapp_number: Optional[str] = None
    whatsapp_enabled: bool = False

class CardAttempt(BaseModel):
    card_id: str
    title: str
    lines_total: int
    lines_completed: int
    accuracy_pct: float
    typo_count: int
    time_seconds: int

class MemorizeAttemptV2(BaseModel):
    groups_selected: List[str]
    cards: List[CardAttempt]
    cards_completed: int
    cards_total: int
    total_time_seconds: int
    overall_accuracy_pct: float

# ── Helper Functions ─────────────────────────────────────────────────────────

def get_student_path(name: str, subject: str = "islamiyat"):
    return os.path.join(STUDENTS_DIR, subject, name.strip().title().replace(" ", "_"))

def trigger_whatsapp_report(phone: str, message: str):
    def run():
        try:
            url = "http://localhost:3001/send-message"
            data = json.dumps({"phone": phone, "message": message}).encode("utf-8")
            req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status == 200:
                    logger.info(f"WhatsApp message sent successfully to {phone}")
        except Exception as e:
            logger.error(f"Failed to send WhatsApp message: {e}")

    threading.Thread(target=run).start()

def load_json(path: str):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to parse JSON at {path}: {e}")
    return None

# ── Endpoints ────────────────────────────────────────────────────────────────

@app.get("/")
async def root():
    return {"message": "Welcome to Nur Academy API", "status": "online"}

@app.get("/api/{subject}/syllabus")
async def get_syllabus(subject: str):
    path = os.path.join(DATA_DIR, subject, "syllabus.json")
    data = load_json(path)
    if data: return data
    logger.error(f"Syllabus not found at {path}")
    raise HTTPException(status_code=404, detail="Syllabus file not found")

@app.get("/api/{subject}/memorize")
async def get_memorize_content(subject: str):
    path = os.path.join(DATA_DIR, subject, "memorize_content.json")
    data = load_json(path)
    if data: return data
    logger.error(f"Memorize content not found at {path}")
    raise HTTPException(status_code=404, detail="Memorize content file not found")

@app.get("/api/{subject}/project_guide")
async def get_project_guide(subject: str):
    path = os.path.join(DATA_DIR, subject, "project_guide.json")
    data = load_json(path)
    if data: return data
    raise HTTPException(status_code=404, detail="No project guide for this subject")

@app.get("/api/{subject}/prep_sessions")
async def get_prep_sessions(subject: str):
    path = os.path.join(DATA_DIR, subject, "prep_sessions.json")
    data = load_json(path)
    if data: return data
    raise HTTPException(status_code=404, detail="No preparation sessions for this subject")

@app.get("/api/students/{student_name}/{subject}/progress")
async def get_student_progress(student_name: str, subject: str):
    path = os.path.join(get_student_path(student_name, subject), "progress_log.json")
    data = load_json(path)
    return data if data else []

@app.post("/api/{subject}/exam/generate")
async def generate_exam(subject: str, setup: ExamSetup):
    logger.info(f"Generating exam for {setup.student_name}...")
    try:
        from tasks.generate_questions import load_all_questions
        all_q = load_all_questions(subject)
    except Exception as e:
        logger.error(f"Import error or file error in tasks: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    pool = []
    for q in all_q:
        section = str(q.get("section", "")).upper()
        source = q.get("source_type", "")
        is_mcq = q.get("type", "").lower() == "mcq"

        if section == "A":
            if source == "Quranic" and not setup.inc_quran: continue
            if source == "Hadith" and not setup.inc_hadith: continue
        elif section == "B" and not setup.inc_b: continue
        elif section == "C" and not setup.inc_c: continue

        if setup.mode == "MCQ only" and not is_mcq: continue
        if setup.mode == "Extended only" and is_mcq: continue

        pool.append(q)

    if not pool:
        logger.warning("Zero questions found matching criteria")
        raise HTTPException(status_code=400, detail="No questions match criteria in the bank.")

    random.shuffle(pool)
    selected = pool[:setup.n_questions]
    
    return {
        "questions": selected,
        "total_available": len(pool),
        "count": len(selected)
    }

@app.post("/api/{subject}/exam/evaluate")
async def evaluate_exam(subject: str, submission: ExamSubmission):
    score = 0
    total_marks = 0
    question_results = []
    section_scores = {}

    for i, q in enumerate(submission.questions):
        marks = q.get("marks", 1)
        total_marks += marks
        student_ans = submission.answers.get(str(i), "")
        correct_ans = q.get("correct_answer", q.get("model_answer", ""))
        qtype = q.get("type", "mcq").lower()
        section = q.get("section", "A")
        source = q.get("source_type", section)

        if section not in section_scores:
            section_scores[section] = {"score": 0, "total": 0, "source": source}
        section_scores[section]["total"] += marks

        if qtype == "mcq":
            correct = student_ans.strip().upper() == str(correct_ans).strip().upper()
        else:
            correct = False

        if correct:
            score += marks
            section_scores[section]["score"] += marks

        topic_label = q.get("surah_name") or q.get("topic") or q.get("hadith_reference") or q.get("topic_name") or source
        question_results.append({
            "question": q.get("question", ""),
            "student_answer": student_ans,
            "correct_answer": correct_ans,
            "correct": correct,
            "marks_earned": marks if correct else 0,
            "topic": topic_label
        })

    percentage = round((score / max(total_marks, 1)) * 100, 1)
    result = {
        "student": submission.student_name,
        "score": score,
        "total": total_marks,
        "percentage": percentage,
        "question_results": question_results
    }

    # Save logic
    student_dir = get_student_path(submission.student_name, subject)
    os.makedirs(os.path.join(student_dir, "attempts"), exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(os.path.join(student_dir, "attempts", f"attempt_{ts}.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    return result

@app.post("/api/students/{student_name}/{subject}/memorize-attempt")
async def log_memorize_attempt(student_name: str, subject: str, attempt: MemorizeAttempt):
    student_dir = get_student_path(student_name, subject)
    os.makedirs(student_dir, exist_ok=True)
    log_path = os.path.join(student_dir, "progress_log.json")
    log = load_json(log_path) or []
    entry = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "mode": "memorize",
        "cards_completed": attempt.cards_completed,
        "cards_total": attempt.cards_total
    }
    log.append(entry)
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)
    return {"status": "success"}

# ── Per-User Progress Helpers ────────────────────────────────────────────────

def get_user_dir(user_id: str) -> str:
    """Return storage dir for a Google-authenticated user, sanitised."""
    safe_id = ''.join(c for c in user_id if c.isalnum() or c == '-')
    return os.path.join(STUDENTS_DIR, safe_id)

def _collect_dates(memorize_log: list, exam_log: list) -> set:
    """Extract unique YYYY-MM-DD strings from both logs."""
    dates = set()
    for entry in memorize_log:
        d = entry.get("date", "")
        if d:
            dates.add(d[:10])  # handle both date and datetime strings
    for entry in exam_log:
        d = entry.get("date", "")
        if d:
            dates.add(d[:10])
    return dates

def compute_streak(memorize_log: list, exam_log: list) -> int:
    """Count consecutive calendar days with activity ending today or most-recent day."""
    dates = _collect_dates(memorize_log, exam_log)
    if not dates:
        return 0
    sorted_dates = sorted(dates, reverse=True)
    today = date.today()
    most_recent = date.fromisoformat(sorted_dates[0])
    # If most recent activity is more than 1 day ago, streak is 0
    if (today - most_recent).days > 1:
        return 0
    streak = 1
    for i in range(1, len(sorted_dates)):
        prev = date.fromisoformat(sorted_dates[i - 1])
        curr = date.fromisoformat(sorted_dates[i])
        if (prev - curr).days == 1:
            streak += 1
        else:
            break
    return streak

def compute_stats(memorize_log: list, exam_log: list) -> dict:
    """Aggregate stats from both logs."""
    total_sessions = len(memorize_log) + len(exam_log)
    total_time = sum(e.get("total_time_seconds", 0) for e in memorize_log)
    total_time += sum(e.get("time_taken", 0) for e in exam_log)
    # Average accuracy from memorize sessions only
    accuracies = [e.get("overall_accuracy_pct", 0) for e in memorize_log if "overall_accuracy_pct" in e]
    avg_accuracy = round(sum(accuracies) / max(len(accuracies), 1), 1)
    return {
        "current_streak": compute_streak(memorize_log, exam_log),
        "total_sessions": total_sessions,
        "avg_accuracy": avg_accuracy,
        "total_time_seconds": total_time,
    }

# ── Per-User Progress Endpoints ──────────────────────────────────────────────

@app.post("/api/users/{user_id}/profile")
async def upsert_user_profile(user_id: str, profile: UserProfile):
    user_dir = get_user_dir(user_id)
    os.makedirs(user_dir, exist_ok=True)
    profile_path = os.path.join(user_dir, "profile.json")
    existing = load_json(profile_path) or {}
    
    # Merge existing values if not provided in request
    whatsapp_number = profile.whatsapp_number if profile.whatsapp_number is not None else existing.get("whatsapp_number")
    whatsapp_enabled = profile.whatsapp_enabled if profile.whatsapp_enabled is not None else existing.get("whatsapp_enabled", False)
    
    data = {
        "name": profile.name,
        "email": profile.email,
        "picture": profile.picture,
        "whatsapp_number": whatsapp_number,
        "whatsapp_enabled": whatsapp_enabled,
        "created_at": existing.get("created_at", datetime.now().isoformat()),
        "updated_at": datetime.now().isoformat(),
    }
    with open(profile_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return {"status": "success"}

@app.get("/api/users/{user_id}/{subject}/progress")
async def get_user_progress(user_id: str, subject: str):
    user_dir = get_user_dir(user_id)
    mem_path = os.path.join(user_dir, subject, "memorize_log.json")
    exam_path = os.path.join(user_dir, subject, "exam_log.json")
    profile_path = os.path.join(user_dir, "profile.json")
    
    memorize_log = load_json(mem_path) or []
    exam_log = load_json(exam_path) or []
    profile = load_json(profile_path) or {}
    
    return {
        "stats": compute_stats(memorize_log, exam_log),
        "memorize_log": memorize_log,
        "exam_log": exam_log,
        "profile": profile,
    }

@app.post("/api/users/{user_id}/{subject}/memorize-attempt")
async def log_user_memorize_attempt(user_id: str, subject: str, attempt: MemorizeAttemptV2):
    user_dir = get_user_dir(user_id)
    subject_dir = os.path.join(user_dir, subject)
    os.makedirs(subject_dir, exist_ok=True)
    log_path = os.path.join(subject_dir, "memorize_log.json")
    log = load_json(log_path) or []
    entry = {
        "session_id": str(uuid.uuid4()),
        "date": datetime.now().isoformat(),
        "groups_selected": attempt.groups_selected,
        "cards": [c.model_dump() for c in attempt.cards],
        "cards_completed": attempt.cards_completed,
        "cards_total": attempt.cards_total,
        "total_time_seconds": attempt.total_time_seconds,
        "overall_accuracy_pct": attempt.overall_accuracy_pct,
    }
    log.append(entry)
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)

    # Trigger WhatsApp Report if enabled
    profile_path = os.path.join(user_dir, "profile.json")
    profile = load_json(profile_path) or {}
    if profile.get("whatsapp_enabled") and profile.get("whatsapp_number"):
        groups = ", ".join(attempt.groups_selected)
        exam_log_path = os.path.join(user_dir, subject, "exam_log.json")
        exam_log = load_json(exam_log_path) or []
        streak = compute_streak(log, exam_log)
        msg = (
            f"📚 *Nur Academy - Memorize Progress Report*\\n\\n"
            f"👤 *Student:* {profile.get('name', 'Student')}\\n"
            f"📖 *Subject:* {subject.title()}\\n"
            f"📝 *Topics:* {groups}\\n"
            f"⏱️ *Duration:* {attempt.total_time_seconds} seconds\\n"
            f"🎯 *Accuracy:* {attempt.overall_accuracy_pct}%\\n"
            f"🏆 *Cards Completed:* {attempt.cards_completed}/{attempt.cards_total}\\n"
            f"🔥 *Current Streak:* {streak} days\\n\\n"
            f"Keep going! 🚀"
        )
        trigger_whatsapp_report(profile["whatsapp_number"], msg)

    return {"status": "success", "session_id": entry["session_id"]}

@app.post("/api/users/{user_id}/{subject}/exam/evaluate")
async def evaluate_user_exam(user_id: str, subject: str, submission: ExamSubmission):
    """Same grading logic as the original evaluate, but saves to user-keyed storage."""
    score = 0
    total_marks = 0
    question_results = []

    for i, q in enumerate(submission.questions):
        marks = q.get("marks", 1)
        total_marks += marks
        student_ans = submission.answers.get(str(i), "")
        correct_ans = q.get("correct_answer", q.get("model_answer", ""))
        qtype = q.get("type", "mcq").lower()

        if qtype == "mcq":
            correct = student_ans.strip().upper() == str(correct_ans).strip().upper()
        else:
            correct = False

        if correct:
            score += marks

        topic_label = q.get("surah_name") or q.get("topic") or q.get("hadith_reference") or q.get("topic_name") or ""
        question_results.append({
            "question": q.get("question", ""),
            "student_answer": student_ans,
            "correct_answer": correct_ans,
            "correct": correct,
            "marks_earned": marks if correct else 0,
            "topic": topic_label,
        })

    percentage = round((score / max(total_marks, 1)) * 100, 1)
    result = {
        "attempt_id": str(uuid.uuid4()),
        "date": datetime.now().isoformat(),
        "score": score,
        "total": total_marks,
        "percentage": percentage,
        "time_taken": submission.time_taken,
        "question_results": question_results,
    }

    # Save to user-keyed storage
    user_dir = get_user_dir(user_id)
    subject_dir = os.path.join(user_dir, subject)
    os.makedirs(subject_dir, exist_ok=True)
    exam_path = os.path.join(subject_dir, "exam_log.json")
    exam_log = load_json(exam_path) or []
    exam_log.append(result)
    with open(exam_path, "w", encoding="utf-8") as f:
        json.dump(exam_log, f, ensure_ascii=False, indent=2)

    # Trigger WhatsApp Report if enabled
    profile_path = os.path.join(user_dir, "profile.json")
    profile = load_json(profile_path) or {}
    if profile.get("whatsapp_enabled") and profile.get("whatsapp_number"):
        mem_log_path = os.path.join(user_dir, subject, "memorize_log.json")
        mem_log = load_json(mem_log_path) or []
        streak = compute_streak(mem_log, exam_log)
        msg = (
            f"📝 *Nur Academy - Exam Results Report*\\n\\n"
            f"👤 *Student:* {profile.get('name', 'Student')}\\n"
            f"📖 *Subject:* {subject.title()}\\n"
            f"📊 *Score:* {score}/{total_marks} ({percentage}%)\\n"
            f"⏱️ *Time Spent:* {submission.time_taken} seconds\\n"
            f"🔥 *Current Streak:* {streak} days\\n\\n"
            f"Keep reviewing to master the topics! 🏆"
        )
        trigger_whatsapp_report(profile["whatsapp_number"], msg)

    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

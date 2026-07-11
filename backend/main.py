import sys
import os
import json
import random
import time
import logging
from datetime import datetime
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

# ── Helper Functions ─────────────────────────────────────────────────────────

def get_student_path(name: str, subject: str = "islamiyat"):
    return os.path.join(STUDENTS_DIR, subject, name.strip().title().replace(" ", "_"))

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

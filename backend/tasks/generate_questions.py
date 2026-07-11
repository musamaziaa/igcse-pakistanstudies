"""Task 3: Generate AI question bank using Claude API."""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils.claude_client import call_claude

BASE = os.path.dirname(os.path.dirname(__file__))
QB_PATH = os.path.join(BASE, "data", "question_bank")

QURAN_PROMPT = """You are an IGCSE Islamiyat MCQ generator for the LRN Global board.

Generate one MCQ per verse for {surah_name} (Surah {surah_number}).
The Surah has {ayat_count} verses.

For each verse:
- Include the Arabic text of that verse
- Include its English translation
- Write a question testing one clear concept from that verse
- Provide 4 answer options (A, B, C, D) — one correct, three plausible distractors
- Flag the correct answer
- Vary the question angle across verses (translation, meaning, theme, linguistic, contextual) — do not repeat the same format consecutively

Return strictly valid JSON array. No preamble. No markdown fences.
Schema per item: section, type, source_type, surah_name, surah_number, ayat_number, arabic_text, english_translation, question, options {{A,B,C,D}}, correct_answer, marks.

section="A", type="MCQ", source_type="Quranic", marks=1
"""

HADITH_PROMPT = """You are an IGCSE Islamiyat MCQ generator for the LRN Global board.

Given this Hadith from the syllabus:
  Arabic:      {hadith_arabic}
  Translation: {hadith_english}
  Reference:   {hadith_reference}

Generate minimum 3 MCQs covering these angles:
1. Translation  – correct meaning of the Arabic text
2. Context      – narrator, collection, or occasion
3. Lesson/Ruling – Islamic teaching or ruling it establishes

For each MCQ include: section, type, source_type, hadith_reference, arabic_text, english_translation, question, options {{A,B,C,D}}, correct_answer, marks.
section="A", type="MCQ", source_type="Hadith", marks=1

Return strictly valid JSON array. No preamble. No markdown fences.
"""

EXTENDED_PROMPT = """You are an IGCSE Islamiyat exam question generator for the LRN Global board.

Context provided:
  Syllabus topic:  {topic_title}
  Subtopics:       {subtopics}

Generate a comprehensive question bank for this topic covering:
1. Fill-in-the-Blank: sentence with one key term missing (include Arabic where term is Arabic)
2. Complete-the-Sentence: opening clause requiring completion
3. Short Answer: 2-4 mark question with model answer
4. Essay/Extended: 8-mark question with level-based mark scheme

Important rules:
- For any event that occurred AFTER the Hijrah (migration to Madinah in 622 CE / 1 AH), always include both the Hijri date (AH) and the CE date. Example: Battle of Badr (2 AH / 624 CE).
- For any battle or military campaign, structure questions and model answers using the CEO pattern:
    C = Cause    — why did this battle occur?
    E = Events   — what happened during the battle?
    O = Outcome  — what were the results and significance?
  Label sections clearly in model answers as "Cause:", "Events:", "Outcome:".

For each question:
- Assign type: "fill_blank" | "complete_sentence" | "short_answer" | "essay"
- Write the question in English
- Include Arabic text where appropriate (always with transliteration + English translation)
- Provide a model answer optimised for LRN mark scheme scoring
- Indicate estimated marks

Return strictly valid JSON array. No preamble. No markdown fences.
Schema per item: section, type, topic_number, topic_title, question, arabic_text, transliteration, english_translation, model_answer, marks.
"""


def _save_json(path: str, data) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _parse_json_response(raw: str) -> list:
    raw = raw.strip()
    if raw.startswith("```"):
        parts = raw.split("```")
        raw = parts[1] if len(parts) > 1 else raw
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()
    return json.loads(raw)


def generate_quran_mcqs(surahs: list, progress_callback=None) -> list:
    """Generate MCQs for all Surahs. Returns flat list of all questions."""
    all_questions = []
    for i, surah in enumerate(surahs):
        if progress_callback:
            progress_callback(i, len(surahs), f"Generating MCQs for {surah['surah_name']}...")
        prompt = QURAN_PROMPT.format(
            surah_name=surah["surah_name"],
            surah_number=surah["surah_number"],
            ayat_count=surah["ayat_count"]
        )
        try:
            raw = call_claude(prompt, max_tokens=4096)
            questions = _parse_json_response(raw)
            slug = surah['surah_name'].lower().replace(' ', '_').replace("'", '')
            path = os.path.join(QB_PATH, "section_a", "quran", f"surah_{surah['surah_number']}_{slug}.json")
            _save_json(path, questions)
            all_questions.extend(questions)
        except Exception as e:
            if progress_callback:
                progress_callback(i, len(surahs), f"Error on {surah['surah_name']}: {e}")
        time.sleep(0.5)
    return all_questions


def generate_hadith_mcqs(ahadith: list, progress_callback=None) -> list:
    """Generate MCQs for all Ahadith."""
    all_questions = []
    for i, hadith in enumerate(ahadith):
        if progress_callback:
            progress_callback(i, len(ahadith), f"Generating MCQs for Hadith {hadith.get('hadith_number', i+1)}...")
        prompt = HADITH_PROMPT.format(
            hadith_arabic=hadith.get("arabic", ""),
            hadith_english=hadith.get("translation", ""),
            hadith_reference=hadith.get("reference", "")
        )
        try:
            raw = call_claude(prompt, max_tokens=2048)
            questions = _parse_json_response(raw)
            path = os.path.join(QB_PATH, "section_a", "hadith", f"hadith_{hadith.get('hadith_number', i+1):03d}.json")
            _save_json(path, questions)
            all_questions.extend(questions)
        except Exception as e:
            if progress_callback:
                progress_callback(i, len(ahadith), f"Error on Hadith {i+1}: {e}")
        time.sleep(0.5)
    return all_questions


def generate_extended_questions(topics: list, section: str, progress_callback=None) -> list:
    """Generate extended questions for Section B or C topics."""
    all_questions = []
    for i, topic in enumerate(topics):
        if progress_callback:
            progress_callback(i, len(topics), f"Generating extended questions for Topic {topic.get('topic_number', i+1)}: {topic.get('title', '')}...")
        prompt = EXTENDED_PROMPT.format(
            topic_title=topic.get("title", ""),
            subtopics=", ".join(topic.get("subtopics", []))
        )
        try:
            raw = call_claude(prompt, max_tokens=4096)
            questions = _parse_json_response(raw)
            slug = topic.get("title", f"topic_{i}").lower()[:30].replace(" ", "_").replace("'", "")
            path = os.path.join(QB_PATH, f"section_{section.lower()}", f"topic_{topic.get('topic_number', i+1)}_{slug}.json")
            _save_json(path, questions)
            all_questions.extend(questions)
        except Exception as e:
            if progress_callback:
                progress_callback(i, len(topics), f"Error on topic {i+1}: {e}")
        time.sleep(0.5)
    return all_questions


def load_all_questions(subject: str = "islamiyat") -> list:
    """Load all questions from question_bank directory."""
    all_q = []
    qb_path = os.path.join(BASE, "data", subject, "question_bank")
    for root, dirs, files in os.walk(qb_path):
        for fname in files:
            if fname.endswith(".json"):
                try:
                    with open(os.path.join(root, fname), encoding="utf-8") as f:
                        data = json.load(f)
                    if isinstance(data, list):
                        all_q.extend(data)
                    elif isinstance(data, dict) and "questions" in data:
                        all_q.extend(data["questions"])
                except Exception:
                    pass
    return all_q


def question_bank_exists() -> bool:
    for root, dirs, files in os.walk(QB_PATH):
        for fname in files:
            if fname.endswith(".json"):
                return True
    return False


def count_questions_by_section() -> dict:
    counts = {"A_quran": 0, "A_hadith": 0, "B": 0, "C": 0}
    for root, dirs, files in os.walk(QB_PATH):
        for fname in files:
            if not fname.endswith(".json"):
                continue
            path = os.path.join(root, fname)
            try:
                with open(path, encoding="utf-8") as f:
                    data = json.load(f)
                n = len(data) if isinstance(data, list) else len(data.get("questions", []))
                if "section_a" in root and "quran" in root:
                    counts["A_quran"] += n
                elif "section_a" in root and "hadith" in root:
                    counts["A_hadith"] += n
                elif "section_b" in root:
                    counts["B"] += n
                elif "section_c" in root:
                    counts["C"] += n
            except Exception:
                pass
    return counts

"""Task 2: Ingest sample paper + mark scheme and pair questions with answers."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils.pdf_parser import extract_text
from utils.claude_client import call_claude

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "sample_paper.json")

SYSTEM = "You are an expert at analysing IGCSE exam papers and mark schemes. Extract structured data accurately."

PROMPT_TEMPLATE = """You are given a sample exam paper and its mark scheme for LRN International GCSE Islamiyat.

Extract and pair each question with its model answer. Return a single valid JSON object:

{{
  "questions": [
    {{
      "section": "A",
      "question_number": "i",
      "question_type": "MCQ",
      "question_text": "...",
      "arabic_text": "...",
      "options": {{"A": "...", "B": "...", "C": "...", "D": "..."}},
      "model_answer": "B",
      "marks": 1
    }},
    {{
      "section": "B",
      "question_number": "1a",
      "question_type": "extended",
      "question_text": "...",
      "arabic_text": "",
      "model_answer": "...",
      "marks": 8
    }}
  ]
}}

Rules:
- For MCQs: include all 4 options and the correct letter as model_answer
- For extended: include a summary of the mark scheme criteria as model_answer
- arabic_text: include any Arabic text in the question (empty string if none)
- question_type: "MCQ", "short_answer", "extended", "fill_blank"
- Return ONLY valid JSON, no preamble, no markdown fences

EXAM PAPER TEXT:
{paper_text}

MARK SCHEME TEXT:
{scheme_text}
"""


def ingest_paper(paper_bytes: bytes, paper_filename: str, scheme_bytes: bytes, scheme_filename: str) -> dict:
    paper_text = extract_text(paper_bytes, paper_filename)
    scheme_text = extract_text(scheme_bytes, scheme_filename)
    prompt = PROMPT_TEMPLATE.format(paper_text=paper_text[:8000], scheme_text=scheme_text[:8000])
    raw = call_claude(prompt, system=SYSTEM, max_tokens=6000)
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    data = json.loads(raw)
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return data


def load_sample_paper() -> dict:
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {}

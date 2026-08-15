"""Distil each subject's LRN spec + past papers + mark schemes into a marking guide.

Run once (and again whenever new papers land in source_docs/):

    ./venv/bin/python backend/scripts/build_grading_guides.py [subject ...]

For each subject it reads every PDF under backend/data/{subject}/source_docs/,
sends the text to Claude, and writes backend/data/{subject}/grading_guide.md —
a condensed examiner's guide (assessment objectives, level/band descriptors,
command words, marking conventions). The exam grader loads that guide at
runtime, so the full PDFs are never sent on a student's request.
"""

import glob
import os
import sys

import anthropic
import fitz  # PyMuPDF
from dotenv import load_dotenv

load_dotenv()

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
SUBJECTS = ["islamiyat", "pak_studies", "hospitality", "cs", "ai", "ict"]

SUBJECT_NAMES = {
    "islamiyat": "LRN International GCSE Islamiyat (2141)",
    "pak_studies": "LRN International GCSE Pakistan Studies (2107)",
    "hospitality": "LRN International GCSE Hospitality (7146)",
    "cs": "LRN International GCSE Computer Science (7925)",
    "ai": "LRN International GCSE Artificial Intelligence (7923)",
    "ict": "LRN International GCSE Information and Communication Technology (7927)",
}

INSTRUCTION = """You are writing a marking guide that another examiner will use to mark student answers for {name}.

The documents above are the official specification, past/sample papers and mark schemes for this qualification. Read them and produce a single reference guide covering ONLY what a marker needs.

Include:

1. **Assessment objectives** — the AOs, what each rewards, and their weighting.
2. **Paper structure** — sections, question types, mark allocations, timing.
3. **Level/band descriptors** — for extended and essay questions, reproduce the actual mark bands from the mark schemes (e.g. what separates a top-band 7-8 mark answer from a 3-4 mark one). This is the most important section: be specific and quote the real wording where the mark schemes give it.
4. **Command words** — what "describe", "explain", "evaluate", "to what extent", "justify" etc. each require, as used in this specification.
5. **Marking conventions** — how marks are awarded per point, when to credit alternatives to the model answer, how partial credit works, treatment of irrelevant or blank answers, and any subject-specific rules (e.g. Islamiyat's handling of Quranic quotation, Computer Science's credit for pseudocode/logic over exact syntax).
6. **Common student errors** the mark schemes call out, and what they cost.

Write it as clean Markdown for an expert reader. Be concrete and specific to this qualification — no generic advice about marking. Do not include the answers to individual past-paper questions; the guide must generalise to unseen questions. Aim for 1200-2500 words."""


def extract_pdfs(subject: str) -> tuple:
    """Return (combined text, list of filenames) for a subject's source docs."""
    root = os.path.join(DATA_DIR, subject, "source_docs")
    parts, names = [], []
    for path in sorted(glob.glob(os.path.join(root, "**", "*.pdf"), recursive=True)):
        try:
            doc = fitz.open(path)
            text = "".join(page.get_text() for page in doc)
            doc.close()
        except Exception as exc:  # a corrupt or image-only PDF shouldn't kill the run
            print(f"    ! skipped {os.path.basename(path)}: {exc}")
            continue
        if not text.strip():
            print(f"    ! skipped {os.path.basename(path)}: no extractable text")
            continue
        rel = os.path.relpath(path, root)
        parts.append(f"===== FILE: {rel} =====\n{text}")
        names.append(rel)
    return "\n\n".join(parts), names


def build(subject: str, client: anthropic.Anthropic) -> None:
    name = SUBJECT_NAMES.get(subject, subject)
    print(f"[{subject}] reading PDFs...")
    text, names = extract_pdfs(subject)
    if not text:
        print(f"[{subject}] no source PDFs found — skipping.")
        return
    print(f"[{subject}] {len(names)} files, {len(text):,} chars -> asking Claude...")

    prompt = f"{text}\n\n{INSTRUCTION.format(name=name)}"

    # Streamed: the input is large and the guide is long, so a non-streaming
    # call risks an HTTP timeout.
    with client.messages.stream(
        model="claude-opus-5",
        max_tokens=16000,
        system="You are a senior LRN International GCSE examiner and chief moderator.",
        output_config={"effort": "high"},
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        response = stream.get_final_message()

    if response.stop_reason == "refusal":
        print(f"[{subject}] refused: {response.stop_details}")
        return

    guide = next((b.text for b in response.content if b.type == "text"), "").strip()
    if not guide:
        print(f"[{subject}] empty response — skipping write.")
        return

    header = (
        f"<!-- Generated by backend/scripts/build_grading_guides.py.\n"
        f"     Source documents: {', '.join(names)}\n"
        f"     Re-run the script to regenerate after adding papers. -->\n\n"
    )
    out = os.path.join(DATA_DIR, subject, "grading_guide.md")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(header + guide + "\n")

    usage = response.usage
    print(
        f"[{subject}] wrote {out} ({len(guide):,} chars) "
        f"[in {usage.input_tokens:,} / out {usage.output_tokens:,} tokens]"
    )


def main() -> None:
    targets = sys.argv[1:] or SUBJECTS
    unknown = [s for s in targets if s not in SUBJECTS]
    if unknown:
        sys.exit(f"Unknown subject(s): {', '.join(unknown)}. Choose from {', '.join(SUBJECTS)}.")

    if not os.getenv("ANTHROPIC_API_KEY"):
        sys.exit("ANTHROPIC_API_KEY is not set (put it in .env at the project root).")

    client = anthropic.Anthropic()
    for subject in targets:
        try:
            build(subject, client)
        except Exception as exc:
            print(f"[{subject}] FAILED: {exc}")


if __name__ == "__main__":
    main()

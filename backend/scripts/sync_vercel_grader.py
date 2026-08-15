"""Copy the generated grading guides into the Vercel function's bundle.

The Vercel grading function (nur-academy/api/grade.py) deploys from the
frontend directory, so it cannot read backend/data at runtime. Run this after
rebuilding the guides:

    ./venv/bin/python backend/scripts/build_grading_guides.py
    ./venv/bin/python backend/scripts/sync_vercel_grader.py
"""

import os
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(ROOT, "backend", "data")
DEST = os.path.join(ROOT, "nur-academy", "api", "grading_guides")
SUBJECTS = ["islamiyat", "pak_studies", "hospitality", "cs", "ai", "ict"]

os.makedirs(DEST, exist_ok=True)
for subject in SUBJECTS:
    src = os.path.join(DATA_DIR, subject, "grading_guide.md")
    if not os.path.exists(src):
        print(f"[{subject}] no grading_guide.md — run build_grading_guides.py first")
        continue
    shutil.copy2(src, os.path.join(DEST, f"{subject}.md"))
    print(f"[{subject}] synced -> api/grading_guides/{subject}.md")

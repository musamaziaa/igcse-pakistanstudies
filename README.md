# Nur Academy: IGCSE Islamiyat & Pakistan Studies Prep

Nur Academy is a high-fidelity, AI-powered study companion designed for the **LRN Global Board IGCSE Islamiyat and Pakistan Studies** examinations. It features a modern, mobile-first design, interactive memorization tools, and a dynamic exam engine.

---

## 🏛️ Architecture: Decoupled Full-Stack
The platform has been migrated from a monolithic Streamlit app to a modern decoupled architecture:
1.  **Backend (FastAPI):** A high-performance Python API that handles AI generation, grading logic, and persistent JSON storage.
2.  **Frontend (Next.js/React):** A beautiful, responsive UI generated via Google Stitch, using Tailwind CSS and Lucide icons.

---

## ✨ Features

### 1 — Memorize Topic (Interactive)
- **Deep Content:** Enriched Topic 2 content (Revelation to Compilation) from detailed study guides.
- **Typing Engine:** A tactile, character-by-character typing practice system.
- **Instant Feedback:** Visual color cues (Green = Correct, Red = Typo) and a pulsing cursor.
- **Arabic Rendering:** High-readability Serif fonts for Quranic verses and Ahadith.

### 2 — Exam Engine
- **Live Generation:** Fetches randomized questions directly from the FastAPI backend.
- **Question Map:** Visual grid to navigate and track answered questions.
- **Real-Time Grading:** Automated scoring of MCQs with immediate performance feedback.

### 3 — Multi-User Dashboard
- Personalized "Assalam-o-Alaikum" landing page.
- Progress tracking saved per-student in `backend/data/students/`.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- Node.js & NPM
- Anthropic API Key (in `.env`)

### Installation & Run
1.  Install Python dependencies: `pip install -r backend/requirements.txt`
2.  Install Frontend dependencies: `cd nur-academy && npm install`
3.  **Run Everything:**
    ```bash
    ./start_nur_academy.sh
    ```

---

## 📁 Project Structure
- `backend/main.py`: The "Brain" (FastAPI Backend).
- `nur-academy/src/App.tsx`: The "Face" (Next.js Frontend).
- `backend/data/`: Shared data store (Syllabus, Question Bank, Student Logs).
- `start_nur_academy.sh`: Unified startup script.

---

## 🛠️ Tech Stack
- **Languages:** TypeScript, Python.
- **Frontend:** Next.js 15, Tailwind CSS, Motion (Framer), Lucide.
- **Backend:** FastAPI, Pydantic, Uvicorn.
- **AI:** Claude 3.5 Sonnet.

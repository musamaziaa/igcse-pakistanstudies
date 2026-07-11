# Project: Nur Academy (IGCSE Islamiyat & Pak Studies Exam Prep)

A modern, full-stack AI-powered study companion for IGCSE Islamiyat and Pakistan Studies. Replaced the original monolithic Streamlit app with a decoupled Next.js + FastAPI architecture for cloud scalability.

## Tech Stack
- **Frontend:** Next.js (App Router), TypeScript, Tailwind CSS, Lucide Icons (Stitch-generated).
- **Backend:** FastAPI (Python 3.12), Pydantic validation, Uvicorn.
- **AI:** Claude 3.5 Sonnet (Anthropic SDK) for question generation and analysis.
- **Storage:** JSON-based data store in `backend/data/`.

## Running the Project
```bash
./start_nur_academy.sh
```
Starts Backend (Port 8000) and Frontend (Port 5173). Logs errors to `backend.log`.

## Core Backend (FastAPI)
| File | Purpose |
|------|---------|
| `backend/main.py` | Central API server (CORS enabled). |
| `/api/syllabus` | GET: Fetches the structured curriculum. |
| `/api/memorize` | GET: Fetches flashcards with enriched Topic 2 content. |
| `/api/exam/generate` | POST: Creates randomized mock exams. |
| `/api/exam/evaluate` | POST: Grades exams and saves results to student profile. |
| `/api/students/{name}/progress` | GET: Retrieves student history. |

## Core Frontend (Next.js)
| File | Purpose |
|------|---------|
| `nur-academy/src/App.tsx` | Main React logic: View switching (Dashboard, Exam, Memorize). |
| **Exam Engine** | State-driven question navigation with real-time feedback. |
| **Memorize Engine** | Character-by-character typing with visual feedback, real-time topic search, and auto-scrolling active lines. |

## Data Schemas
**Memorize Card:** `{id, group_id, group_label, tier_label, title, arabic, lines[], display_category}`
**Exam Result:** `{student, score, total, percentage, question_results[]}`

The frontend types memorize cards via the `MemCard` interface in `nur-academy/src/App.tsx` (not `any[]`). Note: the tier-grouping `.map((groupId: string) => ...)` callback must keep its explicit `string` annotation — without it TS widens the value to `unknown` and `tsc --noEmit` (the `lint` script) fails. Lines must be plain typeable ASCII (no curly quotes / em–en dashes) because the Memorize engine matches input character-by-character; `arabic` is `""` for all Pak Studies cards.

## Memorize Content (`backend/data/{subject}/memorize_content.json`)
**Pak Studies** has 11 topics across 3 tiers (served by `GET /api/pak_studies/memorize`):
- **Tier 1: Critical** — Constitutional Development, Pakistan Movement, Key Dates Timeline, Founding Leaders & Reformers.
- **Tier 2: Most Important** — Foreign Policy, Agriculture/Water & Resources, Physical Geography, Economic Challenges & Development.
- **Tier 3: Nice to Learn** — Current Perspectives, Population & Employment, Nuclear Programme & Global Role.

Tier display order follows JSON insertion order of first appearance, so keep cards grouped by tier in the file. Content is anchored to the LRN 2107 spec, the Nov/Dec 2025 paper + mark scheme, and the revision booklet in `backend/data/source_docs/pak_studies/`.

**Hospitality** (LRN International GCSE Hospitality 7146) has 9 memorize cards across the same 3 tiers (served by `GET /api/hospitality/memorize`), covering the 5 syllabus units: (1) Introduction to the Hospitality Industry, (2) Customer Service Skills, (3) Effective Team Working, (4) Food Preparation & Cooking, (5) Food, Nutrition & Exercise. Section A MCQs use **five** options (A–E), unlike Islamiyat/Pak Studies (A–D); the frontend renders `Object.entries(options)` so this is handled automatically. Content is anchored to the 7146 spec, Sample Paper 1 (+MS) and Sample Paper 2-A (+MS) in `backend/data/source_docs/hospitality/`. `arabic` is `""` for all Hospitality cards.

**Computer Science** (LRN International GCSE 7925, subject key `cs`) has 11 memorize cards across 3 tiers, covering the 3 syllabus units: (1) Systems Architecture, (2) Algorithms, Programming & Logic, (3) Data Representation. Anchored to the 7925 spec and past papers (Nov/Dec 2023–2025, May/June 2025) in `backend/data/source_docs/cs/`.

**Artificial Intelligence** (LRN International GCSE 7923, subject key `ai`) has 9 memorize cards across 3 tiers, covering the 6 syllabus units: (1) Foundations of AI, (2) Machine Learning & Data Science, (3) Knowledge Representation & Reasoning, (4) Planning & Autonomous Systems, (5) Ethics, Society & Philosophy of AI, (6) Building & Deploying AI Systems. Anchored to the 7923 spec, Paper 1 (+MS) and Paper 2 rubric in `backend/data/source_docs/ai/`.

**ICT** (LRN International GCSE Information and Communication Technology 7927, subject key `ict`) has 9 memorize cards across 3 tiers, covering the 6 syllabus units: (1) Types & Components of Computer Systems, (2) Input/Output & Storage Devices, (3) Networks & Applications of ICT, (4) System Development & Security, (5) Document Management & Productivity Tools, (6) Advanced Data Handling & Web Development. Anchored to the 7927 spec and May 2025 papers (+MS) in `backend/data/source_docs/ict/`. CS/AI/ICT cards all use `arabic: ""`.

## Question-Bank Structure Mirrors Each Subject's Real Paper
The A/B/C sectioning is **not** universal — each subject's `question_bank/` reflects its own LRN paper, so do not copy Islamiyat's Section A/B/C onto a new subject by default:
- **Islamiyat** — Section A (Quran/Hadith MCQs), B (short), C (extended).
- **Pak Studies / Hospitality** — Section A MCQs (Hospitality uses A–E), B (short), C (extended).
- **Computer Science & ICT** — Paper 1 is theory only: a single stream of numbered structured/short-answer questions with marks (no sections, **no MCQs**). Files live under `question_bank/paper1_theory/`, grouped by unit. Paper 2 is a practical exam (programming for CS; document production/databases/spreadsheets/web authoring for ICT) and is not modelled as auto-answerable questions. ICT theory covers units 1–4; units 5–6 are the Paper 2 practical.
- **AI** — Paper 1 has **Section A: Knowledge and Understanding** (MCQs + short/structured/extended, A–D options) and **Section B: Analysis and Evaluation** (case study, evaluation, logical reasoning). **No Section C.** Paper 2 is a practical/internal assessment.

Question objects carry `type` (`MCQ`/`short_answer`/`structured`/`extended`/`case_study`/`evaluation`/`logical_reasoning`), `marks`, `model_answer` (or `options`+`correct_answer` for MCQ), and optionally `section`/`section_title`. `load_all_questions(subject)` walks the whole `question_bank` tree, so folder layout is free; the exam engine only auto-grades `MCQ` and shows `model_answer` (self-marked) for everything else.

## Exam UI (non-MCQ)
The exam view in `nur-academy/src/App.tsx` branches on whether a question has `options`: MCQs render as clickable buttons; all other types render a free-text `<textarea>` plus a "Show model answer" reveal (state in `revealed`). A badge row shows `section`/`section_title`, `topic_title`, and `marks`. This makes CS/ICT/AI written questions usable and also fixes Islamiyat/Pak Studies/Hospitality Section B/C, which previously rendered blank.

All six subjects are registered in the `SUBJECTS` config array in `nur-academy/src/App.tsx` (key, display name, Lucide icon, static Tailwind color classes) — add new subjects there rather than hardcoding cards. The backend is subject-agnostic: every endpoint is `/api/{subject}/...` resolving to `backend/data/{subject}/`, so a new subject only needs its data folder plus a `SUBJECTS` entry.

## Project Guide (practical / coursework papers)
Some subjects have a Paper 2 that is **not** an auto-answerable exam in the app — either coursework or a practical/programming paper with no fixed answers. These are documented as a read-only guide, not question-bank entries. An **optional** `backend/data/{subject}/project_guide.json` is served by `GET /api/{subject}/project_guide` (404 when the file is absent). Schema: `{title, subtitle, intro, overview[{label,value}], components[{name, marks?, summary, criteria?[{criterion, marks?}]}], tools[], steps[{title, detail}], submission[], tips[]}` — every top-level array is optional and its section is skipped if missing; within `components`, `marks` and `criteria` (and each criterion's `marks`) are also optional, so the same view renders both a marked coursework rubric (AI) and an exam task-breakdown with no per-task marks (CS/ICT). The frontend fetches it on subject change into `guide` state; when non-null, a violet "Paper 2 Guide" `DashboardCard` appears and opens the generic `project_guide` view.

Three subjects currently ship a guide:
- **AI** — Paper 2 is a supervised, internally-assessed build-an-AI-model **project** (100 marks, 50%); guide reproduces the real Component A/B/C mark rubric.
- **CS** — Paper 2 is a **written Problem-solving & Programming exam** (75 marks, 1h45, equal weight to Paper 1); guide covers the scenario + Task 1–3 pattern and structured questions (no per-task marks published).
- **ICT** — Paper 2 is a **practical software exam** (Document Production, Databases & Presentations; 70 marks, ~2.5h; Units 5–6) using supplied source files; guide covers the Evidence Document + document/database/presentation/printing tasks.

Islamiyat, Pak Studies and Hospitality have no Paper 2 guide (their card stays hidden).

## Preparation Sessions (hands-on Paper 2 walkthroughs)
Separate from (and complementary to) the read-only `project_guide` rubric, a subject can ship **hands-on, click-by-click walkthroughs** — each teaches a complete end-to-end practical project. An **optional** `backend/data/{subject}/prep_sessions.json` is served by `GET /api/{subject}/prep_sessions` (404 when absent). Schema: `{sessions[{id, title, subtitle, project_name?, difficulty?, duration?, intro?, overview?[{label,value}], materials?[], steps[{title, detail?, substeps?[], tip?, illustration?}], evidence?[], ethics_note?, next_up?}]}`. Every session becomes its **own** indigo `Rocket` `DashboardCard` (rendered by `prepSessions.map(...)`); clicking opens the generic `prep_session` view. Each step's `illustration` is a **self-contained inline SVG string** (schematic mock-up of the real software screen) rendered via `dangerouslySetInnerHTML` with `[&_svg]:w-full` so it scales responsively — use single-quoted SVG attributes and no literal newlines so the string stays valid JSON. This is a **list**, so more sessions are added purely as data (no code change); each session is an independent, increasingly advanced project.

**AI** currently ships **Session 1** — a full Google Teachable Machine "Recycling Sorter" (3-class image classifier) built end-to-end (define → collect → clean → train → test → improve → export → document), covering Paper 2 Component A plus the screenshots for Component B. Only AI has `prep_sessions.json`; all other subjects 404 and show no session cards.

## Production Roadmap
Before this prototype can be hosted for real users, see [`ROADMAP.md`](ROADMAP.md) — the single source of truth for the pre-hosting gaps (auth, database, security hardening, deployment) and product features (results screen, AI grading, progress dashboard). Each item lists what's needed, options with pros/cons, and a suggested solution. Keep it updated as items ship.

For **where to host**, see [`hosting.md`](hosting.md) — researched comparison of static-frontend hosts, FastAPI/ASGI backend hosts (PaaS + VPS), and managed databases, with recommended stacks by budget. Key constraint: FastAPI is ASGI, so **Namecheap shared hosting cannot run the backend** (VPS/Dedicated only).

## Legacy Reference
The original Streamlit app has been removed in favor of the full-stack architecture.

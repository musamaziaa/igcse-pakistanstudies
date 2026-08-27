# Project: Nur Academy (IGCSE Exam Prep, six subjects)

A full-stack AI-powered study companion for six LRN International GCSE subjects. Replaced the original monolithic Streamlit app with a decoupled React + FastAPI architecture.

## Tech Stack
- **Frontend:** React 19 SPA built with **Vite** (not Next.js — there is no App Router, no SSR, no `pages/`), TypeScript, Tailwind CSS v4, Lucide icons, Motion for animation.
- **Backend:** FastAPI (Python 3.12), Pydantic validation, Uvicorn.
- **AI:** Anthropic SDK. `claude-opus-5` for exam grading (`utils/ai_grader.py`, `nur-academy/api/grade.py`) and for building the grading guides; `claude-sonnet-4-5` in the legacy offline generation script `utils/claude_client.py`.
- **Storage:** JSON files under `backend/data/`. No database.

## Running the Project
```bash
./start_nur_academy.sh
```
Starts three processes: the WhatsApp gateway (Node, port 3001), the FastAPI backend (port 8000) and the Vite dev server. Note the port mismatch: the script echoes 5173 but `package.json`'s `dev` script binds **3000**; CORS allows both.

## Core Backend (FastAPI)
Every content route is subject-scoped — `/api/{subject}/...` resolving to `backend/data/{subject}/`. There are no unscoped `/api/syllabus` or `/api/memorize` routes.

| Route | Purpose |
|------|---------|
| `backend/main.py` | Central API server (CORS enabled). |
| `GET /api/{subject}/syllabus` | Structured curriculum. |
| `GET /api/{subject}/memorize` | Typing-practice cards. |
| `GET /api/{subject}/memorize_stories` | Story-based revision (404 when absent). |
| `GET /api/{subject}/project_guide` | Paper 2 guide (404 when absent). |
| `GET /api/{subject}/prep_sessions` | Practical walkthroughs (404 when absent). |
| `POST /api/{subject}/exam/generate` | Builds a paper (see **Paper Assembly**). |
| `POST /api/{subject}/exam/evaluate` | Grades and saves anonymously. |
| `POST /api/users/{user_id}/{subject}/exam/evaluate` | Same, saved per signed-in user. |
| `GET /api/users/{user_id}/{subject}/progress` | Stats, streak, memorize + exam logs. |

User-keyed routes are gated by `require_user` (`utils/google_auth.py`), which verifies the Google ID token server-side against `GOOGLE_CLIENT_ID` — decoding the JWT client-side proves nothing.

## WhatsApp Reports (`backend/whatsapp_service/`)
A Node/Baileys microservice on port 3001, launched by `start_nur_academy.sh`. After a memorize or exam session, `main.py` fires a progress report at it in a background thread (`trigger_whatsapp_report`) when the user's profile has `whatsapp_enabled` and a number. Failures are logged and ignored — the service being down never breaks a request.

## Core Frontend (React + Vite)
| File | Purpose |
|------|---------|
| `nur-academy/src/App.tsx` | The entire app in one ~1900-line file: view switching, all engines, auth. |
| **Exam Engine** | State-driven navigation; MCQ buttons or free-text textarea with model-answer reveal. |
| **Memorize Engine** | Character-by-character typing with visual feedback, topic search, auto-scrolling active lines. |
| **Stories Engine** | Read-only story reader with Story / Key Points / Quiz tabs. |

**`@types/react` is not installed and `tsconfig.json` sets no `strict`/`noImplicitAny`.** React imports therefore resolve to `any`, so `npm run lint` (`tsc --noEmit`) type-checks almost nothing in `App.tsx` — it passes even with a wrong `useState` union member. Treat a clean `tsc` as weak evidence; `npm run build` and actually loading the page are the real checks.

## Data Schemas
**Memorize Card:** `{id, group_id, group_label, tier_label, title, arabic, lines[], display_category}`
**Exam Result:** `{student, score, total, percentage, question_results[]}`

The frontend types memorize cards via the `MemCard` interface in `nur-academy/src/App.tsx` (not `any[]`).

Three rules the Memorize engine actually depends on:

1. **`lines` must be plain typeable ASCII** — no curly quotes, em/en dashes, arrows or emoji — because the engine matches input character-by-character. `arabic` is `""` for every non-Islamiyat subject.
2. **`tier_label` must be set on every card.** The picker groups by `c.tier_label || "Other Topics"`, so a null tier silently dumps the card into one flat untiered bucket. Islamiyat had all 93 cards at `null` for a while and lost its tiering entirely.
3. **A `group_id` must not span two tiers.** The picker lists groups per tier and labels each from the *first* card with that id, so a group split across tiers appears twice under the wrong name, and ticking either copy selects all of its cards.

## Memorize Content (`backend/data/{subject}/memorize_content.json`)
Current card counts (Tier 1 / 2 / 3): Islamiyat 104 (57/31/16) · AI 19 (7/6/6) · Pak Studies 18 (6/7/5) · Hospitality 15 (7/5/3) · CS 11 (5/3/3) · ICT 9 (3/3/3).

**Pak Studies** has 18 cards across 3 tiers (served by `GET /api/pak_studies/memorize`), covering the constitutional, historical, geographic and economic units. The original 11 are:
- **Tier 1: Critical** — Constitutional Development, Pakistan Movement, Key Dates Timeline, Founding Leaders & Reformers.
- **Tier 2: Most Important** — Foreign Policy, Agriculture/Water & Resources, Physical Geography, Economic Challenges & Development.
- **Tier 3: Nice to Learn** — Current Perspectives, Population & Employment, Nuclear Programme & Global Role.

Tier display order follows JSON insertion order of first appearance, so keep cards grouped by tier in the file. Content is anchored to the LRN 2107 spec, the Nov/Dec 2025 paper + mark scheme, and the revision booklet in `backend/data/pak_studies/source_docs/`.

**Hospitality** (LRN International GCSE Hospitality 7146) has 15 memorize cards across the same 3 tiers (served by `GET /api/hospitality/memorize`), covering the 5 syllabus units: (1) Introduction to the Hospitality Industry, (2) Customer Service Skills, (3) Effective Team Working, (4) Food Preparation & Cooking, (5) Food, Nutrition & Exercise. Section A MCQs use **five** options (A–E), unlike Islamiyat/Pak Studies (A–D); the frontend renders `Object.entries(options)` so this is handled automatically. Content is anchored to the 7146 spec, Sample Paper 1 (+MS) and Sample Paper 2-A (+MS) in `backend/data/hospitality/source_docs/`. `arabic` is `""` for all Hospitality cards.

**Computer Science** (LRN International GCSE 7925, subject key `cs`) has 11 memorize cards across 3 tiers, covering the 3 syllabus units: (1) Systems Architecture, (2) Algorithms, Programming & Logic, (3) Data Representation. Anchored to the 7925 spec and past papers (Nov/Dec 2023–2025, May/June 2025) in `backend/data/cs/source_docs/`.

**Artificial Intelligence** (LRN International GCSE 7923, subject key `ai`) has 19 memorize cards across 3 tiers, covering the 6 syllabus units: (1) Foundations of AI, (2) Machine Learning & Data Science, (3) Knowledge Representation & Reasoning, (4) Planning & Autonomous Systems, (5) Ethics, Society & Philosophy of AI, (6) Building & Deploying AI Systems. Anchored to the 7923 spec, Paper 1 (+MS) and Paper 2 rubric in `backend/data/ai/source_docs/`.

**ICT** (LRN International GCSE Information and Communication Technology 7927, subject key `ict`) has 9 memorize cards across 3 tiers, covering the 6 syllabus units: (1) Types & Components of Computer Systems, (2) Input/Output & Storage Devices, (3) Networks & Applications of ICT, (4) System Development & Security, (5) Document Management & Productivity Tools, (6) Advanced Data Handling & Web Development. Anchored to the 7927 spec and May 2025 papers (+MS) in `backend/data/ict/source_docs/`. CS/AI/ICT cards all use `arabic: ""`.

## Question-Bank Structure Mirrors Each Subject's Real Paper
The A/B/C sectioning is **not** universal — each subject's `question_bank/` reflects its own LRN paper, so do not copy Islamiyat's Section A/B/C onto a new subject by default:
- **Islamiyat** (spec **2141**) — Section A (Quran/Hadith MCQs), B (short), C (extended).
- **Pak Studies / Hospitality** — Section A MCQs (Hospitality uses A–E), B (short), C (extended). Hospitality also has **Paper 2-A**, a 50-mark scenario-based *written* paper — unlike CS/ICT/AI Paper 2 it is fully auto-gradeable, and lives in `question_bank/paper2a/` with `section: "Paper 2A"` and `type: "case_study"`.
- **Computer Science & ICT** — Paper 1 is theory only: a single stream of numbered structured/short-answer questions with marks (no sections, **no MCQs**). Files live under `question_bank/paper1_theory/`, grouped by unit. Paper 2 is a practical exam (programming for CS; document production/databases/spreadsheets/web authoring for ICT) and is not modelled as auto-answerable questions. ICT theory covers units 1–4; units 5–6 are the Paper 2 practical.
- **AI** — Paper 1 has **Section A: Knowledge and Understanding** (MCQs + short/structured/extended, A–D options) and **Section B: Analysis and Evaluation** (case study, evaluation, logical reasoning). **No Section C.** Paper 2 is a practical/internal assessment.

Question objects carry `type` (`MCQ`/`short_answer`/`structured`/`extended`/`case_study`/`evaluation`/`logical_reasoning`), `marks`, `model_answer` (or `options`+`correct_answer` for MCQ), and optionally `section`/`section_title`/`mark_scheme`. Files are either a bare JSON array or `{"questions": [...]}` — `load_all_questions(subject)` accepts both and walks the whole `question_bank` tree, so folder layout is free.

Current bank sizes: Islamiyat 199 q / 516 marks · Hospitality 158 / 587 · Pak Studies 110 / 307 · AI 70 / 253 · CS 29 / 104 · ICT 21 / 72. **CS and ICT are the thin ones** — ICT's whole bank is smaller than one 80-mark paper, so every generated ICT paper is identical until more questions land.

Islamiyat carries 61 one-mark `fill_blank` questions. No LRN paper uses that format, so they are **deliberately excluded from assembled papers** — the Islamiyat blueprint lists Section B/C types as `short_answer`/`extended`/`essay`, and a full paper contains none of them. They are kept on purpose as recall drilling and surface only in **Quick practice**, which is the right home for them. Keep it that way: don't add `fill_blank` to a blueprint's `types`, and don't delete the questions.

## Paper Assembly (`POST /api/{subject}/exam/generate`)
`PAPER_BLUEPRINTS` in `backend/main.py` records each subject's real paper — total marks, duration, and the mark budget and allowed question types per section, read off the papers in `source_docs/`:

| Subject | Marks | Minutes | Sections |
|---|---|---|---|
| Islamiyat | 70 | 150 | A 20 · B 25 · C 25 |
| Pak Studies | 50 | 150 | A 15 · B 20 · C 15 |
| Hospitality | 50 | 60 | A 10 · B 25 · C 15 |
| CS | 75 | 105 | single theory stream |
| ICT | 80 | 90 | single theory stream |
| AI | 100 | 105 | A 60 · B 40 |

`build_paper()` fills each section via `_fill_section()`, which draws **weighted at random by marks** — a heavy question is likelier to be picked, so a 25-mark section gets an essay rather than twenty-five 1-mark items, while still differing between attempts. A final pass looks for a question worth exactly the remaining marks so sections land on their real total where the bank allows.

`ExamSetup.paper_mode` is `"full"` (default) or `"quick"` (the old `n_questions` random draw, still offered in the UI as *Quick practice*). If a bank cannot fill even half the paper — or a filter such as `mode="MCQ only"` strips the sections out — it logs a warning and **falls back to random selection** rather than failing. The response adds `paper`, `target_marks`, `total_marks`, `duration_minutes` and a `sections[]` summary, which the exam header renders.

Note the questions the builder emits carry `section_title` set to the blueprint's full title (e.g. `"Section A: Multiple Choice"`), so the exam badge renders `section_title` alone — prefixing it with `Section {section}` double-prints.

## Exam Grading
`grade_submission(subject, submission)` in `backend/main.py` is the single grading path for **both** evaluate endpoints (anonymous and user-keyed) — don't reimplement it per endpoint. MCQs are graded by comparing the student's option letter to `correct_answer` (falling back to `model_answer`, which is what Pak Studies MCQs use). Every other type goes to `backend/utils/ai_grader.py`, which marks the whole paper in **one** Claude call (`claude-opus-5`, `output_config.format` structured outputs, effort `medium`) against each question's `model_answer` + `marks`, returning partial credit and per-question feedback.

### Grading guides (the mark scheme Claude marks against)
`backend/data/{subject}/source_docs/` holds the official LRN PDFs (spec, past/sample papers, mark schemes) downloaded from lrnschools.org — ~28 MB across the six subjects. Those PDFs are **never** sent at request time. Instead `backend/scripts/build_grading_guides.py` distils each subject's whole document set into `backend/data/{subject}/grading_guide.md` (~15-20 KB): assessment objectives, paper structure, the real level/band descriptors quoted from the mark schemes, command-word requirements, marking conventions and common errors. Re-run it (`./venv/bin/python backend/scripts/build_grading_guides.py [subject ...]`) whenever new papers are added; it overwrites the guide.

`ai_grader.load_grading_guide()` reads the guide once per subject per process and appends it to the system prompt as a second block carrying `cache_control` — the stable global instructions render first, so the breakpoint caches both. Verified: second and subsequent submissions for a subject read ~6.5K tokens from cache instead of re-sending them. A missing guide is non-fatal — grading falls back to the `model_answer` alone and logs a warning.

### Two grading paths — backend-side and Vercel-side
`ExamSubmission.ai_marks` is optional. When present (`{"<index>": {marks_awarded, feedback}}`) `grade_submission` uses those marks and does **not** call Anthropic; when absent it calls `ai_grader` itself. This exists because free PythonAnywhere's outbound allowlist excludes `api.anthropic.com`, so in production the browser calls the Vercel function `nur-academy/api/grade.py` first and passes the marks through. `grade.py` mirrors `ai_grader.py` — **keep `SYSTEM_PROMPT` and `RESULT_SCHEMA` in sync between them**, and run `backend/scripts/sync_vercel_grader.py` after regenerating guides so `nur-academy/api/grading_guides/` matches. Supplied marks are clamped to each question's `marks` but are otherwise trusted; see `DEPLOY.md` for why that's acceptable here and when it wouldn't be.

Critical invariant: **a question's marks only enter `total` once it has actually been graded.** If the AI grader is unavailable (`GradingUnavailable` — missing `ANTHROPIC_API_KEY`, API error, or a `refusal` stop reason) those questions are flagged `graded_by: "ungraded"` and their marks are reported as `ungraded_marks` instead of being counted as wrong. Before this, non-MCQs were hardcoded `correct = False` while still inflating the denominator, capping real scores at 13.7% (Islamiyat) to 0% (CS/ICT, which have no MCQs).

The response adds `objective`/`written` `{score,total}` splits, `section_scores`, `ai_grading` `{status,detail}` (`ok`/`partial`/`unavailable`), and per-question `marks`, `marks_earned`, `graded_by`, `feedback`. The frontend types these as `QuestionResult` and renders them in the `session_result` view as a "Marked Answers" panel. Requires `ANTHROPIC_API_KEY` in the environment or a `.env` the backend can load.

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

**AI** currently ships **three sessions**, all building the *same* "Recycling Sorter" (3-class Paper/Plastic/Metal image classifier) with a different tool each time, so students can compare the approaches in their Component B report. Each is 10 steps with an illustration per step, and each runs the full pipeline (define → collect → clean → train → test → improve → export → document):
- **Session 1 — Google Teachable Machine** (Beginner, 2-3h): no-code, click-driven.
- **Session 2 — Google Colab** (Intermediate, 3-4h): Python/TensorFlow transfer learning from a frozen MobileNetV2 base; illustrations are mock Colab notebook cells showing the real code and its output.
- **Session 3 — Scratch + AI extension blocks** (Beginner-Intermediate, 2-3h): trains on Machine Learning for Kids, then wires the model into a Scratch 3 program; ends with a three-tool comparison table.

Session `next_up` fields chain 1 → 2 → 3, and sessions are stored sorted by `id`. Only AI has `prep_sessions.json`; all other subjects 404 and show no session cards.

## Memorize with Stories (`memorize_stories.json`)
A second, **read-only** revision mode that lives inside the Memorize view (not a dashboard card). An **optional** `backend/data/{subject}/memorize_stories.json` is served by `GET /api/{subject}/memorize_stories` (404 when absent), fetched into `stories` state on subject change; the section only renders when the array is non-empty.

Schema: `{title, subtitle, source, stories[{id, title, unit, unit_title, lesson, lesson_title, tier_label, starred?, summary, paragraphs[], key_points[{moment, exam_point}], quiz[{question, answer, source}]}]}`.

The reader (`activeStory` state) has three tabs — **Story** (narrative), **Key Points** (each story moment mapped to the exam point it carries) and **Quiz** (question with a *Show answer* reveal, plus *Reveal all*). Each panel is capped at `max-h-[65vh]` and scrolls internally; without that the longest stories make the page tall enough to break screenshot capture. Stories are sorted by tier then lesson, so JSON order drives tier display order exactly as it does for memorize cards.

**Only Hospitality ships this today**: 27 stories, 577 paragraphs, 328 key points, 180 quiz questions, covering all 13 lessons and all 5 units. It is extracted from the story-first course book in `backend/data/hospitality/reference/`. Quiz items come from two places, labelled in the UI: the book's *Stop and Think* prompts (the book poses these but never answers them — the answers here were written for this repo) and its *Test Yourself* questions, whose answers the book supplies. Each lesson's 10 Test Yourself items are shared round-robin across that lesson's stories so no two stories repeat the same quiz.

## Source material: `source_docs/` vs `reference/`
Two per-subject folders, both gitignored, holding ~46 MB that never ships:

- **`backend/data/{subject}/source_docs/`** — official LRN PDFs only (spec, papers, mark schemes). `build_grading_guides.py` reads **this tree**, so anything dropped here is sent to Claude on every guide rebuild.
- **`backend/data/{subject}/reference/`** — teaching and course material that is *not* an exam-board document (the Hospitality story-first course, Islamiyat topic notes, the AI reading list). Deliberately outside `source_docs/` because the Hospitality book alone is ~348k characters and would dominate every future guide rebuild while adding no mark-scheme detail.

`Docs/` at the repo root is a gitignored drop zone for newly downloaded PDFs before they are filed into one of the two. Keep it empty between sessions.

Adding questions does **not** make a grading guide stale — the guide is generated from `source_docs/` alone and generalises to unseen questions. Only new source PDFs justify a rebuild.

## Production Roadmap
For deployment steps see [`DEPLOY.md`](DEPLOY.md) (GitHub + Vercel + PythonAnywhere, free tier).

Before this prototype can be hosted for real users, see [`ROADMAP.md`](ROADMAP.md) — the single source of truth for the pre-hosting gaps (auth, database, security hardening, deployment) and product features (results screen, AI grading, progress dashboard). Each item lists what's needed, options with pros/cons, and a suggested solution. Keep it updated as items ship.

For **where to host**, see [`hosting.md`](hosting.md) — researched comparison of static-frontend hosts, FastAPI/ASGI backend hosts (PaaS + VPS), and managed databases, with recommended stacks by budget. Key constraint: FastAPI is ASGI, so **Namecheap shared hosting cannot run the backend** (VPS/Dedicated only).

## Legacy Reference
The original Streamlit app has been removed in favor of the full-stack architecture.

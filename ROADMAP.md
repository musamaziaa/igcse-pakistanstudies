# Nur Academy — Production Roadmap

**Status:** Planning · **Last updated:** 2026-07-03
**Purpose:** Single source of truth for what stands between the current local prototype and a portal that can be safely hosted for real users. CLAUDE.md links here; keep this file updated as decisions are made or items ship.

## How to read this
Each item lists:
- **What's needed** — the gap, grounded in current code.
- **Options** — candidate solutions with **Pros / Cons**.
- **✅ Suggested** — the recommended choice and why.
- **Status** — `TODO` / `IN PROGRESS` / `DONE` / `DEFERRED`.

Priority tiers: 🔴 **Blocker** (unsafe/broken to host without) · 🟠 **Important** (product feels broken) · 🟡 **Roadmap** (needed to operate as a service).

Current relevant facts:
- Backend: FastAPI, single-file `backend/main.py`, JSON-file storage under `backend/data/`.
- Frontend: React SPA `nur-academy/src/App.tsx`, Vite, `API_BASE` hardcoded to `http://127.0.0.1:8000`.
- AI: Anthropic SDK wired via `backend/utils/claude_client.py` but only used by offline generation scripts, not the live API.
- Identity: free-text student name, no auth.

---

## 🔴 Blockers

### B1. Authentication & user identity — `TODO`
**What's needed:** Today a "user" is just a typed name (`App.tsx:41`, default `"Baba"`). Anyone can read/overwrite anyone's data. Existing data already shows identity collisions (`Waiz`/`WAiz`/`baba`/`Baba`). Need real accounts, sessions, and per-user data isolation.

**Options:**
1. **Managed auth provider (Clerk / Auth0 / Supabase Auth)**
   - Pros: Fastest to ship; handles password reset, email verification, OAuth, MFA, security patching; offloads liability.
   - Cons: External dependency + recurring cost; vendor lock-in; another SDK in the frontend.
2. **Roll our own JWT auth in FastAPI** (`passlib` bcrypt + `python-jose`, HTTP-only cookie sessions)
   - Pros: No vendor cost/lock-in; full control; small dependency footprint.
   - Cons: We own all the security-sensitive surface (reset flows, token rotation, breach risk); more code and tests.
3. **Magic-link / passwordless email**
   - Pros: No password storage; low-friction for students.
   - Cons: Requires reliable transactional email; slower login UX.

**✅ Suggested:** **Option 1 with Supabase Auth**, because B2 already recommends Supabase Postgres — one vendor covers auth + DB, and its Row Level Security ties naturally into per-user isolation. Fall back to Option 2 (self-hosted JWT) only if we must avoid external services entirely.

---

### B2. Persistent database (replace JSON files) — `TODO`
**What's needed:** Attempts and progress are written as JSON files on local disk (`main.py:196–218`). This loses data on redeploy (ephemeral disks), races on concurrent writes (read-modify-write, no lock), and can't scale past one instance.

**Options:**
1. **Managed Postgres (Supabase / Neon / RDS)** via SQLAlchemy + Alembic migrations
   - Pros: Durable, transactional, scales; industry standard; free tiers exist; pairs with B1.
   - Cons: Requires a schema + migration discipline; a real dependency to operate.
2. **SQLite file**
   - Pros: Zero-config, easy local dev.
   - Cons: Still a file on ephemeral disk; weak concurrent writes; doesn't solve the core problem for hosting.
3. **Document store (MongoDB / Firestore)**
   - Pros: Maps almost 1:1 to current JSON shapes; minimal reshaping.
   - Cons: Weaker relational querying for progress analytics; another paradigm to learn.

**✅ Suggested:** **Option 1, managed Postgres (Supabase).** Model `students`, `exam_attempts`, `question_results`, `memorize_attempts` as tables. Content (syllabus/question banks/memorize cards) can **stay as versioned JSON in the repo** — it's read-only reference data, not user data.

**Migration note:** write a one-off script to import existing `backend/data/students/**` into the DB, de-duplicating the name-collision folders.

---

### B3. Input sanitization & API hardening — `TODO`
**What's needed:** `subject` and `student_name` flow straight from the request into `os.path.join()` (`main.py:68, 87, 95, 103`). `.title().replace(" ","_")` does **not** strip `/` or `..`, so a crafted `student_name` is a **path-traversal write** via `/exam/evaluate`. Also CORS is `allow_origins=["*"]` **with** `allow_credentials=True` (`main.py:30–37`) — invalid/insecure — and there is no rate limiting.

**Options:**
1. **Validate against an allow-list + lock CORS to the real origin + add `slowapi` rate limiting**
   - Pros: Directly closes each hole; small, targeted change; no new infra.
   - Cons: Must remember to extend the allow-list when adding subjects (low cost).
2. **Rely on a WAF / API gateway for traffic filtering**
   - Pros: Centralized protection, DDoS mitigation.
   - Cons: Doesn't fix the traversal logic bug itself; added infra/cost; belt without the braces.

**✅ Suggested:** **Option 1.** Concretely: constrain `subject` to a known set (`islamiyat|pak_studies|hospitality`), derive the on-disk/user key from validated input only (once B2 lands, `student_name` stops being a filesystem path at all), set CORS to the deployed frontend origin, and add per-IP + per-user rate limits on `generate`/`evaluate`/AI endpoints. Layer a WAF later as defense-in-depth.

---

### B4. Environment-based frontend config — `TODO`
**What's needed:** `const API_BASE = "http://127.0.0.1:8000"` (`App.tsx:24`) breaks the moment it's deployed.

**Options:**
1. **Vite build-time env var** (`import.meta.env.VITE_API_BASE`)
   - Pros: Standard Vite pattern; per-environment builds; zero runtime cost.
   - Cons: Baked at build time — a URL change needs a rebuild.
2. **Runtime config** (fetch `/config.json` or inject `window.__CONFIG__` at container start)
   - Pros: One build, many environments; change URL without rebuild.
   - Cons: Extra request/plumbing; mild complexity.

**✅ Suggested:** **Option 1** for now (simple, matches Vite conventions). Revisit Option 2 only if we run many environments from one artifact.

---

### B5. Real deployment topology — `TODO`
**What's needed:** `start_nur_academy.sh` runs **dev servers** (`vite dev`, single-process `uvicorn`). Hosting needs a built SPA, a production ASGI server, HTTPS, and reproducible packaging. `backend/static/` exists but is empty/unwired (an abandoned "serve SPA from FastAPI" attempt).

**Options:**
1. **Split hosting:** SPA on static/CDN host (Vercel/Netlify/Cloudflare Pages) + API as a container (`gunicorn -k uvicorn.workers.UvicornWorker`) on Render/Railway/Fly.
   - Pros: Each tier scales independently; CDN for the frontend; clean separation.
   - Cons: Two deploy targets; CORS/config must be managed across origins.
2. **Single container:** FastAPI serves the built SPA from `backend/static/`.
   - Pros: One deployable, one origin (CORS mostly moot); simplest ops.
   - Cons: No CDN edge caching for assets; API and web scale together.
3. **PaaS-managed (e.g., a single Dockerfile on Fly.io/Railway)**
   - Pros: Least ops overhead; HTTPS handled for you.
   - Cons: Some platform lock-in.

**✅ Suggested:** **Option 2 (single container) to launch** — least moving parts, wires up the already-present `backend/static/`, sidesteps cross-origin config — then graduate to **Option 1** if/when frontend traffic or asset caching justifies a CDN. Ship a `Dockerfile` either way.

---

## 🟠 Important (core product)

### I1. Exam results screen — `TODO`  ← highest value-per-effort
**What's needed:** `submitExam` discards the returned `{score, percentage, question_results}` and just `alert("Exam Submitted!")` (`App.tsx:118–127`). Users never see how they did — even though the backend already computes and returns everything.

**Options:**
1. **Add a `results` view** rendering score, per-question correct/incorrect, and the correct answer.
   - Pros: Pure frontend; backend unchanged; large perceived-value jump.
   - Cons: None material.
2. **Also persist + let users revisit past results** (depends on B2).
   - Pros: History, review, retakes.
   - Cons: Needs the DB first.

**✅ Suggested:** **Option 1 now** (independent of the blockers, so it can ship first), extend to **Option 2** after B2. Recommend building this first as a quick, visible win.

---

### I2. Free-text answers + AI grading (Sections B/C) — `TODO`
**What's needed:** Only MCQs are auto-graded; short/scenario answers score 0 and have no input field. Claude is already wired (`claude_client.py`) but unused at runtime. This is the natural differentiator.

**Options:**
1. **LLM-graded free text:** add a textarea; grade the answer against `model_answer` + marks via Claude, returning a score + rubric feedback.
   - Pros: Standout feature; reuses existing SDK; real formative feedback.
   - Cons: API cost + latency; needs prompt design, guardrails, and cost caps (see R6); grading variance to manage.
2. **Self-assessment:** show model answer, let the student self-mark.
   - Pros: Zero AI cost; trivial to build.
   - Cons: Not automated; weaker product story.
3. **Keyword/rubric heuristic scoring**
   - Pros: Cheap, deterministic.
   - Cons: Poor for essay-style answers; brittle.

**✅ Suggested:** **Option 1**, gated behind auth + rate limits + a per-user usage cap (R6), with **Option 2 as a graceful fallback** when the AI budget is exhausted or the call fails. Use the latest appropriate Claude model; pin the model id in config.

---

### I3. Progress dashboard — `TODO`
**What's needed:** `/api/students/{name}/{subject}/progress` is populated but nothing renders it. No trends, no weak-topic view.

**Options:**
1. **Charts (Recharts/Chart.js)** — scores over time, per-topic accuracy.
   - Pros: Clear value; libraries are mature.
   - Cons: A dependency; needs enough data to be meaningful.
2. **Simple table/summary cards** — latest scores, counts.
   - Pros: Minimal; fast.
   - Cons: Less engaging.

**✅ Suggested:** **Start with Option 2** (summary cards) alongside I1, add **Option 1 charts** once the DB (B2) makes richer aggregation easy.

---

### I4. Real exam timer — `TODO`
**What's needed:** `time_taken: 300` is hardcoded (`App.tsx:123`) though a `Timer` icon is imported.

**✅ Suggested:** Implement a client-side timer that records real elapsed time (and optionally enforces a limit), or remove the timer affordance entirely. Low effort; do it alongside I1. No alternatives worth cataloguing.

---

## 🟡 Roadmap (operate as a service)

### R1. Secrets & config management — `TODO`
**What's needed:** `ANTHROPIC_API_KEY` via `.env` is fine locally; production must use the host's secret store and never commit secrets. Confirm `.env` is gitignored.
**✅ Suggested:** Host-provided secret manager (Render/Railway/Fly secrets or cloud KMS); keep a committed `.env.example` documenting required vars.

### R2. Error handling & observability — `TODO`
**What's needed:** Frontend uses `alert()`; backend logging is minimal; no error tracking or health checks.
**Options:** Sentry (frontend+backend) vs. host-native logs only.
**✅ Suggested:** Sentry for error tracking + structured logs + a `/health` endpoint. Replace `alert()` with in-UI toasts/states.

### R3. Backups & data retention — `TODO`
**✅ Suggested:** Enable managed automated DB backups (comes with Supabase/Neon/RDS) once B2 lands; define a retention policy.

### R4. Automated tests & CI — `TODO`
**What's needed:** No tests today.
**✅ Suggested:** pytest for API endpoints (esp. auth, sanitization, grading) + keep `tsc --noEmit` green; run both in GitHub Actions on PRs.

### R5. Legal / compliance — `TODO`
**What's needed:** It's student exam-prep, so the audience may include minors. Need privacy policy, terms, and data-protection posture (GDPR-style), plus parental-consent consideration.
**✅ Suggested:** Draft Privacy Policy + Terms before public launch; minimize stored PII; document lawful basis and retention. (Not legal advice — get review if scaling.)

### R6. AI cost controls — `TODO`
**What's needed:** Generation + I2 grading are unmetered spend/abuse vectors.
**✅ Suggested:** Per-user quotas, request rate limits (ties to B3), response caching where possible, and budget alerts on the Anthropic account.

### R7. Repo cleanup — `TODO`
**What's needed:** Legacy `backend/app.py` (1806-line Streamlit), root scripts (`add_topics.py`, `fix_tiers.py`, `generate_ps_data.py`), and `streamlit` in `requirements.txt` are dead weight.
**✅ Suggested:** Remove/relocate legacy Streamlit code and drop `streamlit` from requirements; move one-off data scripts into a `scripts/` dir or delete once their output is committed.

---

## Suggested sequencing
1. **I1 Results screen** + **I4 timer** — visible wins, no backend changes, ship first.
2. **B1 Auth + B2 Database** — the real foundation; do together (shared Supabase choice).
3. **B3 Sanitization/CORS/rate-limit** — folds in naturally once identity moves to the DB.
4. **B4 env config + B5 Docker/deploy** — get it live.
5. **I2 AI grading** + **I3 dashboard** — the differentiators, on top of the DB.
6. **R1–R7** — harden and operationalize continuously.

## Decision log
- 2026-07-03 — Document created from the pre-hosting gap assessment. No implementation started yet. Open question for owner: acceptable to depend on a managed provider (Supabase) vs. fully self-hosted?

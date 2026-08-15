# Deploying Nur Academy (GitHub + Vercel + PythonAnywhere)

Free-tier setup. Three pieces:

| Piece | Host | Cost |
|---|---|---|
| Frontend (React/Vite) | Vercel | free |
| AI marking (`/api/grade`) | Vercel serverless function | free |
| Backend (FastAPI) + data | PythonAnywhere | free |

## Why marking runs on Vercel, not the backend

Free PythonAnywhere accounts can only reach sites on an
[allowlist](https://www.pythonanywhere.com/whitelist/), and `api.anthropic.com`
is **not** on it. Vercel functions have unrestricted egress, so the Anthropic
call lives in `nur-academy/api/grade.py`. The key is a Vercel environment
variable and never reaches the browser.

```
browser ──> POST /api/grade            (Vercel)  ──> api.anthropic.com
        └─> POST /api/{subject}/exam/evaluate  (PythonAnywhere)  ──> saves marks
```

If PythonAnywhere ever allowlists `api.anthropic.com`
([request form](https://help.pythonanywhere.com/pages/RequestingAllowlistAdditions/)),
the backend grades on its own — it already falls back to `backend/utils/ai_grader.py`
whenever the request arrives without `ai_marks`. No code change needed.

---

## 1. Push to GitHub

```bash
git add -A
git commit -m "AI exam grading"
git push
```

`.env` is gitignored — confirm your key is not in the repo:

```bash
git grep -I "sk-ant-" || echo "clean"
```

## 2. Backend on PythonAnywhere

1. **Bash console** → clone and install:
   ```bash
   git clone https://github.com/<you>/<repo>.git
   cd <repo>
   python3 -m venv venv && source venv/bin/activate
   pip install -r backend/requirements.txt
   ```
2. Set environment variables for the web app (Web tab → Environment variables):

   | Name | Value |
   |---|---|
   | `GOOGLE_CLIENT_ID` | your Google OAuth client ID — **required**, requests 500 without it |
   | `ALLOWED_ORIGINS` | your Vercel URL, e.g. `https://your-app.vercel.app` |
   | `ANTHROPIC_API_KEY` | optional; only used if PythonAnywhere allowlists Anthropic |

3. **Web tab** → ASGI website (FastAPI support is in
   [beta](https://help.pythonanywhere.com/pages/ASGICommandLine/)); point it at
   `backend/main.py`, app object `app`.
4. Note your URL: `https://<you>.pythonanywhere.com`.
5. Reload after every `git pull`.

The JSON data store works as-is — PythonAnywhere has a persistent disk.

**Not deployable there:** the WhatsApp gateway is Node; PythonAnywhere is Python-only.

## 3. Frontend + marking on Vercel

1. Import the GitHub repo at [vercel.com/new](https://vercel.com/new).
2. **Root Directory: `nur-academy`** (this is the step people miss).
3. Environment variables:

   | Name | Value |
   |---|---|
   | `ANTHROPIC_API_KEY` | your key — used by `/api/grade` only, server-side |
   | `GOOGLE_CLIENT_ID` | your Google OAuth client ID — `/api/grade` verifies callers with it |
   | `VITE_API_BASE` | `https://<you>.pythonanywhere.com` |
   | `VITE_GOOGLE_CLIENT_ID` | the same client ID, for the sign-in button |
   | `GRADE_RATE_LIMIT_PER_HOUR` | optional, default `20` papers per user per hour |

4. Deploy. `nur-academy/requirements.txt` makes Vercel build the Python function.

## 4. Connect the two

On PythonAnywhere, set one more environment variable and reload — **no code
edit needed**:

| Name | Value |
|---|---|
| `ALLOWED_ORIGINS` | `https://your-app.vercel.app` (comma-separated if several) |

Without this the browser blocks every API call and the app looks empty.

## 5. Verify

```bash
curl https://your-app.vercel.app/api/grade         # {"status":"ok", "guides":[...]}
curl https://<you>.pythonanywhere.com/api/ai/memorize | head -c 200
```

Then take an exam and submit. Written answers should come back with marks and
feedback. If they show "not assessed", grading failed — check the Vercel
function logs and that `ANTHROPIC_API_KEY` is set there.

---

## Rebuilding the grading guides

The marking guides are generated from the exam-board PDFs in
`backend/data/{subject}/source_docs/` (gitignored — 24 MB). After adding papers:

```bash
./venv/bin/python backend/scripts/build_grading_guides.py   # regenerate
./venv/bin/python backend/scripts/sync_vercel_grader.py     # copy into the Vercel bundle
```

Commit the changed `grading_guide.md` / `nur-academy/api/grading_guides/*.md`.

---

## Known gaps before real users

**Fixed:**

- **Sign-in is verified server-side.** Every `/api/users/{user_id}/...` route
  requires `Authorization: Bearer <Google ID token>`; the backend checks the
  signature against Google's keys and that the token's `sub` matches the
  `user_id` in the path (`backend/utils/google_auth.py`). Wrong user → 403,
  missing or forged token → 401.
- **`/api/grade` is no longer open.** It requires the same verified token and
  caps each account at `GRADE_RATE_LIMIT_PER_HOUR` papers.

**Still open:**

1. **Marks are client-supplied.** The browser passes `ai_marks` to the backend;
   a signed-in student could alter their own marks. Fine for self-study, not
   for anything that counts. Fix by having the backend grade directly (it
   already can — see the fallback path).
2. **The grade rate limit is per Vercel instance,** not global, so the true
   ceiling is the limit × the number of running instances. Use Vercel KV or
   Upstash for an exact cap.
3. **Data is JSON files on disk.** No backups. `ROADMAP.md` B2 covers moving to
   a database.

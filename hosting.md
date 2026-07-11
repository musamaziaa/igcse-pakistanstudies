# Nur Academy — Hosting Options

**Researched:** 2026-07-03 · **Pricing basis:** public pages as of July 2026 — **verify before buying, prices change often.**
**Companion doc:** see [`ROADMAP.md`](ROADMAP.md) for the production gaps (auth, DB, hardening) this hosting must eventually support.

## What this app actually needs (evaluation criteria)
The project is **two services**, which is the single biggest factor in choosing a host:

1. **Frontend** — a **static Vite React SPA** (`nur-academy`). Builds to plain files (`vite build` → `dist/`). Runs anywhere that serves static files. *(Note: CLAUDE.md calls it "Next.js" but it is Vite/SPA — no server runtime needed.)*
2. **Backend** — **FastAPI, which is ASGI** (`backend/main.py`). Needs either a long-running ASGI process (uvicorn/gunicorn) or an ASGI-capable serverless runtime. **This is the constraint that rules out most cheap shared hosting.**
3. **Storage** — currently **JSON files on disk** → needs a **persistent disk**. Many cheap PaaS free tiers use *ephemeral* disks that wipe on redeploy, so JSON storage silently loses data there. This disappears as a constraint once ROADMAP **B2** moves data to a database.
4. **AI (optional, not yet at runtime)** — Anthropic API key, separate paid service. See "Extra costs" below.

---

## ⛔ Key finding: Namecheap **shared** hosting will NOT work
Namecheap's own support states: **"ASGI Python applications are not supported on Shared hosting plans and can be set up only on VPS or Dedicated Servers."** Shared hosting runs Python via **Passenger WSGI**, and FastAPI is ASGI — it cannot run correctly under WSGI without losing async behaviour. So the shared plan at `namecheap.com/hosting/shared` **cannot host the backend.** (You *could* still put the static frontend there.)

To use Namecheap for the whole app you'd need their **VPS** (root access), not shared hosting.

---

## Option comparison

### A. Frontend (static SPA) hosts
| Host | Free tier | Cost if paid | Fit |
|---|---|---|---|
| **Cloudflare Pages** | **Unlimited bandwidth**, 500 builds/mo, free SSL + DDoS + global CDN | Pro tiers optional | ✅ **Best free choice** |
| **Netlify** | 100 GB/mo, 300 build credits/mo | $19/mo Pro | ✅ Good |
| **Vercel** | 100 GB/mo, but **Hobby = non-commercial only** | $20/mo Pro for commercial | ⚠️ Watch the commercial-use rule |
| **Namecheap shared** | included with plan | plan price | ✅ Works for static; poor value vs. free CDN hosts |

**✅ Suggested frontend host: Cloudflare Pages** — free, unlimited bandwidth, no egress fees, global CDN. Nothing beats it for a static SPA.

### B. Backend (FastAPI ASGI) hosts — PaaS
| Host | Free / entry | Persistent disk? | Notes |
|---|---|---|---|
| **Railway** | Hobby **$5/mo** (incl. $5 usage credit); $5 one-time trial | Yes (volumes) | Auto-detects Python; simplest DX; good all-rounder |
| **Render** | Free web service **spins down after 15 min idle**, ~1 min cold start, **no persistent disk on free** | Paid only, disk $0.25/GB/mo | Paid starts **$7/mo per service**; solid but pricier |
| **Fly.io** | **No free tier** (2 VM-hrs / 7-day trial); ~**$1.94/mo** minimal always-on machine | Volumes $0.15/GB/mo (first 10 GB free) | Docker-based; cheapest always-on if you want to migrate to containers later |
| **PythonAnywhere** | $10/mo Developer | Yes | **ASGI/FastAPI is experimental** here — not recommended for production yet |
| **Vercel (serverless)** | Hobby free | ❌ **stateless** | FastAPI deployable, but cold starts + **no persistent disk** (breaks JSON storage; needs external DB); non-commercial on free |

**✅ Suggested backend PaaS: Railway ($5/mo)** — native Python detection, supports a persistent volume (so current JSON storage survives), cheapest predictable all-in-one. Fly.io is a close second if/when you containerise.

### C. Backend (FastAPI) hosts — VPS (full control, run anything incl. Docker)
| Host | Cheapest | 2 vCPU / 4 GB | Notes |
|---|---|---|---|
| **Hetzner Cloud** | from ~€4.51/mo | CPX22 ~€7.99/mo (~$9.49 after Apr 2026) | **Best value**; EU network; IPv6 default |
| **DigitalOcean** | $4/mo basic droplet | $24/mo | Easiest UX + huge docs; managed DB/App Platform available |
| **Namecheap VPS (Quasar)** | ~$11.88–15.88/mo (4 CPU / 4–6 GB) | — | Only Namecheap tier that can run FastAPI; managed +$5–10/mo |

A VPS runs **both** services + a database on one box, matches ROADMAP **B5 Option 2** (single Docker container), and gives persistent disk for the current JSON storage — at the cost of you managing the server (updates, HTTPS, backups).

**✅ Suggested VPS: Hetzner** for value, or **DigitalOcean** if you want the gentlest ops experience.

### D. Database (needed for ROADMAP B2, not for the current JSON prototype)
| Option | Free tier | Notes |
|---|---|---|
| **Neon (Postgres)** | 0.5 GB, 100 CU-hrs/mo, **auto-suspends after 5 min** (auto-resumes) | Best for intermittent traffic; up to 100 projects |
| **Supabase (Postgres + Auth + Storage)** | 500 MB DB, 50K MAU auth, 1 GB files; **pauses after 1 week idle** (manual unpause) | Best if you also want its bundled **Auth** (ties to ROADMAP B1) |
| **Host-provided MySQL** | included on VPS/shared | Fine, but MySQL not Postgres |

**✅ Suggested DB: Supabase** if you adopt its Auth for B1 (one vendor for auth + DB); **Neon** if you only need the database.

---

## Recommended stacks (pick by goal)

### 1. Cheapest that actually works — **~$5/mo** ✅ recommended to start
- Frontend → **Cloudflare Pages** (free)
- Backend → **Railway Hobby** ($5/mo, persistent volume keeps current JSON storage)
- DB → not yet; add **Neon/Supabase free** when you do ROADMAP B2
- **Total: ~$5/mo** + domain. No Docker/server admin needed.

### 2. Most control / one box — **~$8–12/mo**
- Everything on a **Hetzner** (or DigitalOcean) **VPS**, single Docker container (ROADMAP B5 Option 2), Postgres on the same box, Caddy/Nginx for HTTPS.
- **Total: ~€8/mo (Hetzner) or ~$24/mo (DigitalOcean 2vCPU/4GB)** + domain. You manage the server.

### 3. All-Namecheap — **~$12–26/mo**
- Requires **Namecheap VPS** (Quasar ~$11.88/mo unmanaged, or +$5–10 managed). Shared hosting is **not** an option for the backend.
- Static frontend can sit on the same VPS or on free Cloudflare Pages.
- **Total: ~$12–26/mo** + domain. Only worth it if you specifically want everything under Namecheap.

---

## Extra costs beyond hosting
- **Anthropic (Claude) API — separate, usage-based, NOT needed for the current app.** The AI is only used by *offline* content-generation scripts; the live app serves pre-generated JSON and grades MCQs locally. You start paying Anthropic only when you build **AI grading of written answers** (ROADMAP I2) or regenerate question banks. Budget from usage; add cost caps (ROADMAP R6).
- **Domain name** — ~$10/yr (Namecheap or any registrar). Often bundled with hosting.
- **SSL/HTTPS** — free everywhere recommended above (Cloudflare, Railway, Let's Encrypt on VPS).
- **Managed DB** — free tiers (Neon/Supabase) cover launch; paid tiers ~$19–25/mo when you outgrow them.

## Bottom line
- **Shared hosting (the plan you linked) can't run the FastAPI backend** — Namecheap confirms ASGI is VPS/Dedicated only.
- For a cheap, low-maintenance launch: **Cloudflare Pages (frontend) + Railway (backend) ≈ $5/mo**, no server admin, current JSON storage still works.
- If you prefer one server you fully control: a **Hetzner VPS ≈ €8/mo**, matching the roadmap's Docker plan.
- **No extra API purchase is required to run the app today**; Anthropic API is only for the future AI-grading feature.

---

## Sources
- Render pricing: https://render.com/pricing · https://render.com/docs/free
- Railway pricing: https://railway.com/pricing · https://docs.railway.com/pricing/free-trial
- Fly.io pricing: https://fly.io/pricing/ · https://fly.io/docs/about/pricing/
- PythonAnywhere ASGI/FastAPI: https://help.pythonanywhere.com/pages/ASGICommandLine/
- Cloudflare Pages / Netlify / Vercel free tiers: https://www.devtoolreviews.com/reviews/vercel-vs-netlify-vs-cloudflare-pages-pricing-comparison-2026 · https://pages.cloudflare.com/
- Vercel FastAPI + limits: https://vercel.com/docs/frameworks/backend/fastapi · https://vercel.com/docs/functions/limitations
- Namecheap Python/FastAPI support: https://www.namecheap.com/support/knowledgebase/article.aspx/10048/2182/how-to-work-with-python-app/ · https://www.namecheap.com/hosting/shared/
- Namecheap VPS pricing: https://www.namecheap.com/hosting/vps/
- Hetzner vs DigitalOcean: https://betterstack.com/community/guides/web-servers/digitalocean-vs-hetzner/
- Neon vs Supabase free tiers: https://agentdeals.dev/database-free-tier-comparison-2026

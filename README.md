# UpNext — The Daily Operating System for AI Engineers

> An AI-native intelligence platform that filters, ranks, and summarizes the latest in AI engineering — so professionals stay ahead without drowning in Twitter/X, Reddit, GitHub, and newsletters.

**🔗 Live demo:** https://frontend-one-wheat-dw5aauswjr.vercel.app/

---

## The Problem

AI engineers lose hours every week scattered across X, Reddit, Hacker News, GitHub trending, and arXiv trying to keep up with a field that moves daily. The signal-to-noise ratio is brutal. UpNext collapses all of that into one personalized, ranked, summarized feed — a daily habit instead of a daily scramble.

This is **not** a news aggregator or a chatbot wrapper. It's a personalized intelligence layer: collect → filter → rank → summarize → personalize.

---

## Status

🚧 In active development, built in versioned phases.

- ✅ **Phase 1** — Landing page + design system, deployed live on Vercel.
- ✅ **Phase 2** — JWT authentication: FastAPI backend (signup/login/protected routes) + Next.js login/signup pages + protected dashboard.
- ⬜ Phase 3 — AI engineer onboarding + preferences
- ⬜ Phase 4 — Dashboard + personalized feed (mock data)
- ⬜ Phase 5 — Feed/preferences APIs + full Postgres integration
- ⬜ Phase 6 — AI summaries + assistant (Groq)
- ⬜ Phase 7 — Real ingestion pipelines + ranking, polish, final deploy

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 16 (App Router), TypeScript, TailwindCSS v4, Framer Motion |
| Backend | FastAPI (Python 3.12), SQLAlchemy 2.0, Alembic |
| Database | PostgreSQL (Neon, with pgvector planned) |
| Auth | JWT (PyJWT) + bcrypt password hashing |
| AI (Phase 6+) | Groq — Llama 3.3 70B, free-tier inference |
| Hosting | Vercel (frontend), Render (backend, planned), Neon (DB) |

---

## Architecture

Decoupled monolith — two independent deployables, no premature microservices:

```
Next.js 16 (Vercel)  ⇄  FastAPI (Render)  ⇄  PostgreSQL (Neon)
   presentation          auth + AI + API       data + vectors
```

The AI layer (Groq calls) runs server-side only — API keys never reach the browser. The schema is shaped from day one for pgvector-based personalization in later phases without rework.

### Auth flow

1. Signup/login hit FastAPI, which hashes the password (bcrypt) and issues a signed JWT.
2. The frontend stores the token and sends it as a `Bearer` header on protected calls.
3. `GET /auth/me` resolves the token to a user; protected routes 401 without a valid token.
4. The Next.js dashboard guards client-side by calling `/auth/me` on mount and redirecting unauthenticated users to `/login`.

---

## Setup

```bash
# --- Backend ---
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1        # Windows PowerShell
pip install -r requirements.txt
# Create backend/.env from .env.example (DATABASE_URL, JWT_SECRET)
alembic upgrade head               # run migrations against Neon
uvicorn app.main:app --reload      # http://127.0.0.1:8000  (docs at /docs)

# --- Frontend ---
cd frontend
pnpm install
# Create frontend/.env.local with: NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
pnpm dev                           # http://localhost:3000
```

---

## Technical Decisions

- **PyJWT instead of python-jose** — FastAPI's docs moved to PyJWT and python-jose is effectively unmaintained (no release in ~3 years). PyJWT is actively maintained and is what Neon's own FastAPI auth guide uses.
- **Groq instead of OpenAI** — OpenAI-SDK-compatible (drop-in via a custom base URL) but with a zero-cost free tier, keeping the MVP at $0 without changing application code.
- **Two deployables, not microservices** — a clean monolith respects the "don't over-engineer" constraint while keeping the Python AI layer where the strongest skills are.
- **Neon over Supabase** — serverless Postgres with native `pgvector` and branching, without bundling an auth/storage product the app doesn't use (FastAPI owns auth).
- **Dual login endpoints** — a JSON `/auth/login` for the frontend and an OAuth2 form `/auth/token` so the Swagger `/docs` Authorize button works for manual API testing.
- **bcrypt pinned to 4.0.x** — passlib hasn't been updated for bcrypt 4.1+, which otherwise throws a version-read error.

### Security note (known tradeoff)

The MVP stores the JWT in `localStorage` and guards protected routes client-side. This is simple and fine for a portfolio demo, but `localStorage` is readable by XSS and client-side guards don't protect server-rendered data. A production hardening path: move the token to an httpOnly cookie and enforce protection in Next.js middleware. Documented here deliberately rather than hidden.

---

## What Didn't Work / Lessons

- **PowerShell here-strings mangle JSX/nested quotes** — escaped quotes and `>` chars get corrupted or save empty files. Author multi-line code in the editor or via clean file transfer, never through `@"..."@`.
- **PowerShell `Out-File` encoding** — default UTF-8 writes a BOM; `-Encoding ascii` keeps bytes clean.
- **pnpm v11 blocks build scripts by default** — `sharp`, `esbuild`, `unrs-resolver` need explicit `pnpm approve-builds`.
- **Neon connection strings** — use the **direct** (non-pooled) string for Alembic migrations; the pooled host can break them.
- **Swagger Authorize ≠ JSON login** — the OAuth2 Authorize button posts form-encoded data, incompatible with a JSON-body login endpoint; needed a separate `/auth/token` form endpoint.
- **`NEXT_PUBLIC_` env vars load only at dev-server startup** — creating `.env.local` while `pnpm dev` is already running yields `undefined` and a "Failed to fetch"; restart required.

---

## Repository Structure

```
upnext/
├── frontend/                  # Next.js 16 app
│   ├── app/
│   │   ├── (landing)          # marketing homepage
│   │   ├── login/ signup/     # auth pages
│   │   └── dashboard/         # protected route group
│   ├── components/
│   │   ├── marketing/         # landing sections
│   │   └── auth/              # shared auth form
│   └── lib/                   # api client, cn() utility
└── backend/                   # FastAPI
    ├── app/
    │   ├── core/              # config, security (JWT, hashing)
    │   ├── models/            # SQLAlchemy models
    │   ├── schemas/           # Pydantic schemas
    │   ├── routers/           # auth endpoints
    │   ├── db/                # session + Base
    │   └── deps.py            # get_current_user dependency
    └── alembic/               # migrations
```

---

## Roadmap

Personalization grows from simple tag-overlap filtering to vector-similarity ranking over pgvector, once real ingestion from GitHub, arXiv, Reddit, and Hacker News is in place. The architecture supports expansion to other professional niches later, but the MVP is focused exclusively on AI engineers.

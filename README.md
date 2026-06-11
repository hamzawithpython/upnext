# UpNext — The Daily Operating System for AI Engineers

> An AI-native intelligence platform that ingests, filters, ranks, and summarizes the latest in AI engineering — so professionals stay ahead without drowning in Twitter/X, Reddit, GitHub, and newsletters.

**🔗 Live demo:** https://frontend-one-wheat-dw5aauswjr.vercel.app/

---

## The Problem

AI engineers lose hours every week scattered across Hacker News, arXiv, GitHub trending, and HuggingFace trying to keep up with a field that moves daily. The signal-to-noise ratio is brutal. UpNext collapses all of that into one personalized, ranked, AI-summarized feed — a daily habit instead of a daily scramble.

This is **not** a news aggregator or a chatbot wrapper. It's a personalized intelligence layer: ingest → dedup → summarize → rank → personalize.

---

## Status — MVP complete

Built end-to-end in seven versioned phases, each its own feature branch merged to a always-deployable `main`.

- ✅ **Phase 1** — Landing page + design system, deployed on Vercel.
- ✅ **Phase 2** — JWT authentication: FastAPI backend (signup/login/protected routes) + Next.js auth pages + protected dashboard.
- ✅ **Phase 3** — AI engineer onboarding: multi-step preference capture persisted to `user_preferences`, with routing guards.
- ✅ **Phase 4** — Personalized feed UI: ranked feed cards served from a `/feed` endpoint, ranked by tag-overlap with the user's preferences.
- ✅ **Phase 5** — Postgres-backed feed: a `feed_items` table + idempotent seed replace the in-memory mock list. Frontend untouched (the API contract held).
- ✅ **Phase 6** — AI layer (Groq): LLM-generated summaries (structured JSON) and a streaming assistant chat grounded in user preferences.
- ✅ **Phase 7** — Multi-source ingestion: a pipeline pulling from Hacker News, arXiv, GitHub, and HuggingFace, orchestrated on a schedule by an n8n workflow.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 16 (App Router), TypeScript, TailwindCSS v4, Framer Motion |
| Backend | FastAPI (Python 3.12), SQLAlchemy 2.0, Alembic |
| Database | PostgreSQL (Neon) |
| Auth | JWT (PyJWT) + bcrypt |
| AI | Groq — Llama 3.3 70B, free-tier inference |
| Ingestion sources | Hacker News, arXiv, GitHub, HuggingFace |
| Orchestration | n8n (scheduled trigger → ingestion endpoint) |
| Hosting | Vercel (frontend), Neon (DB); backend runs locally |

---

## Architecture

Decoupled monolith — clean separation, no premature microservices:

```
Next.js 16 (Vercel)  ⇄  FastAPI  ⇄  PostgreSQL (Neon)
   presentation         auth · feed · AI · ingest

         n8n (every 6h)
              │  POST /ingest  (shared-secret auth)
              ▼
      FastAPI ingestion pipeline
        ├─ fetch: Hacker News · arXiv · GitHub · HuggingFace
        ├─ normalize → common RawItem shape
        ├─ dedup against feed_items (by source + external id)
        ├─ summarize new items with Groq (structured JSON)
        └─ insert into Postgres → surfaces in the feed
```

**Design split:** n8n owns scheduling/orchestration; FastAPI owns fetching, normalization, dedup, AI summarization, and storage. Source auth and parsing stay in Python (one `.env`, testable), while the automation layer stays simple. Adding a source means writing one fetcher that returns `RawItem`s — nothing else in the pipeline changes.

### Auth flow
Signup/login hit FastAPI, which hashes the password (bcrypt) and issues a signed JWT. The frontend stores the token and sends it as a `Bearer` header; `/auth/me` resolves it. The dashboard guards client-side and redirects unauthenticated or un-onboarded users.

### Personalization
Tag-overlap ranking: feed items are scored by how many of their tags intersect the user's interests + tools, tie-broken by impact then recency. The schema is shaped for a future pgvector similarity upgrade without rework.

---

## Setup

```bash
# --- Backend ---
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1            # Windows PowerShell
pip install -r requirements.txt
# Create backend/.env from .env.example (DATABASE_URL, JWT_SECRET, GROQ_API_KEY,
# GITHUB_TOKEN, HF_TOKEN, INGEST_SECRET, ...)
alembic upgrade head                   # run migrations
python -m app.seed_feed                # seed initial feed items
uvicorn app.main:app --reload          # http://127.0.0.1:8000  (docs at /docs)

# --- Frontend ---
cd frontend
pnpm install
# Create frontend/.env.local: NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
pnpm dev                               # http://localhost:3000

# --- Ingestion (n8n) ---
# Import backend/n8n/upnext-ingestion.workflow.json into n8n.
# It POSTs to host.docker.internal:8000/ingest on a schedule with the
# x-ingest-secret header. Run the backend on the host for it to reach.
```

---

## Technical Decisions

- **PyJWT, not python-jose** — python-jose is effectively unmaintained; PyJWT is current and is what FastAPI's docs and Neon's guides use.
- **Groq, not OpenAI** — OpenAI-SDK-compatible but with a free tier, keeping the project at $0. `GROQ_MODEL` is a config value, not hardcoded, because Groq rotates/deprecates models frequently — a deprecation is a one-line `.env` change.
- **Two deployables, not microservices** — a clean monolith respecting the no-over-engineering constraint, keeping the Python AI layer where the strongest skills are.
- **Neon over Supabase** — serverless Postgres with branching and native pgvector, without an auth/storage product the app doesn't use.
- **n8n orchestrates, FastAPI processes** — the automation tool handles scheduling; OAuth flows, source parsing, and LLM calls stay in Python where they're testable and keys live in one place.
- **Dual login endpoints** — JSON `/auth/login` for the frontend and an OAuth2 form `/auth/token` so the Swagger Authorize button works.
- **Structured JSON LLM output + resilience** — summaries use Groq's JSON mode, with a retry-then-fallback so a single malformed response never crashes a batch ingestion run.
- **Preferences/tags as Postgres arrays** — simpler than join tables for a fixed tag vocabulary with no per-tag relational queries.

### Security notes (known tradeoffs)
- JWT is stored in `localStorage` and routes are guarded client-side — fine for an MVP, but XSS-readable. Production hardening: httpOnly cookies + middleware-enforced protection.
- The `/ingest` endpoint uses a shared-secret header (machine-to-machine), not user JWT, since n8n isn't a logged-in user.
- X (Twitter) ingestion was scoped out — no usable free API tier as of 2026. Reddit was deferred due to API-app-creation friction. Both fit the pluggable source model whenever added.

---

## What Didn't Work / Lessons

- **A backend 500 strips CORS headers**, so the browser reports a "blocked by CORS policy" error even when CORS is fine. Chased CORS for two rounds when the real cause was a Pydantic validation error (`/feed` 500'd because the `Source` literal was missing `"huggingface"`). Lesson: when you see CORS errors but the server is up, check the backend terminal for a 500 first.
- **LLM JSON mode is not a guarantee** — Groq occasionally emitted invalid JSON (unquoted string values), 500-ing the whole ingestion batch. Batch jobs calling an LLM per item need per-item error isolation plus a retry/fallback.
- **Swagger's example bodies corrupt real data** — running a `PUT` from the `/docs` example writes the literal `"string"` into the record; this silently wiped a test user's preferences and surfaced later as the assistant "not knowing" the user.
- **`host.docker.internal`** is how a container (n8n) reaches a service on the host (FastAPI); `127.0.0.1` inside a container means the container itself. Also watch for **port collisions** between projects — another container already held port 8000.
- **PowerShell here-strings mangle JSX/nested quotes** and silently write empty files; author code via clean file transfer. `Out-File` defaults to a BOM — use `-Encoding ascii`.
- **pnpm v11 blocks build scripts by default** (`sharp`, `esbuild`, `unrs-resolver`) — needs `pnpm approve-builds`.
- **Neon: use the direct (non-pooled) connection string for Alembic.**
- **arXiv requires https + follow_redirects; GitHub search syntax is picky** — OR'd topic qualifiers with a date floor returned 422; a free-text query with `pushed:>` and `stars:>` works.
- **`NEXT_PUBLIC_` env vars load only at dev-server startup** — created while `pnpm dev` runs, they read `undefined`.

---

## Repository Structure

```
upnext/
├── frontend/                  # Next.js 16
│   ├── app/                   # landing, login, signup, onboarding, dashboard
│   ├── components/            # marketing, auth, feed, assistant
│   └── lib/                   # api client, utils
└── backend/                   # FastAPI
    ├── app/
    │   ├── core/              # config, security
    │   ├── models/            # users, preferences, feed_items
    │   ├── schemas/           # pydantic
    │   ├── routers/           # auth, preferences, feed, assistant, ingest
    │   ├── services/          # groq_service
    │   ├── ingestion/         # types + per-source fetchers + pipeline
    │   └── db/
    ├── alembic/               # migrations
    └── n8n/                   # exported ingestion workflow
```

---

## Roadmap

Personalization can move from tag-overlap to vector similarity over pgvector. Additional sources (Reddit, X, Product Hunt) plug into the existing pipeline. The architecture supports expansion to other professional niches, but the MVP is focused on AI engineers.

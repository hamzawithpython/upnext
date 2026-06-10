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
- ⬜ Phase 2 — Authentication (FastAPI JWT + protected routes)
- ⬜ Phase 3 — AI engineer onboarding + preferences
- ⬜ Phase 4 — Dashboard + personalized feed (mock data)
- ⬜ Phase 5 — Backend APIs + Postgres integration
- ⬜ Phase 6 — AI summaries + assistant (Groq)
- ⬜ Phase 7 — Real ingestion pipelines + ranking, polish, final deploy

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 16 (App Router), TypeScript, TailwindCSS v4, Framer Motion |
| Backend (Phase 5+) | FastAPI (Python 3.12) |
| Database (Phase 5+) | PostgreSQL (Neon, with pgvector) |
| AI (Phase 6+) | Groq — Llama 3.3 70B, free-tier inference |
| Hosting | Vercel (frontend), Render (backend), Neon (DB) |

---

## Architecture

Decoupled monolith — two independent deployables, no premature microservices:

```
Next.js 16 (Vercel)  ⇄  FastAPI (Render)  ⇄  PostgreSQL (Neon)
   presentation          business + AI         data + vectors
```

The AI layer (Groq calls) runs server-side only — API keys never reach the browser. The schema is shaped from day one for pgvector-based personalization in later phases without rework.

---

## Setup

```bash
# Frontend
cd frontend
pnpm install
pnpm dev          # http://localhost:3000
```

Requires Node 20+, pnpm. Environment variables (Phase 2+) go in `frontend/.env.local`; backend secrets in `backend/.env` (both gitignored — see `.env.example` when added).

---

## Technical Decisions

- **Groq instead of OpenAI** — OpenAI-SDK-compatible, so it's a drop-in replacement via a custom base URL, but with a zero-cost free tier. Keeps the MVP at $0 without changing application code. Llama 3.3 70B on the free tier (30 RPM / 1K requests-per-day) is ample for portfolio-scale summaries and assistant chat.
- **Two deployables, not microservices** — a clean monolith respects the "don't over-engineer" constraint while keeping the Python AI layer where the strongest skills are, instead of forcing AI logic into Next.js API routes.
- **Neon over Supabase** — serverless Postgres with native `pgvector` and branching, without bundling an auth/storage product the app doesn't use (FastAPI owns auth).
- **Tailwind v4 with CSS-based `@theme` tokens** — single source of truth for the dark design system; utility classes (`bg-brand`, `text-fg-muted`) are auto-generated from CSS variables, no JS config file.
- **Manual `cn()` + on-demand shadcn** — skipped the full shadcn `init` to avoid the v3/v4 config mismatch; pull individual primitives only as needed.

---

## What Didn't Work / Lessons

- **PowerShell here-strings mangle JSX** — escaped quotes and `>` characters got corrupted or silently saved empty files when piping component code through PowerShell. Lesson: author multi-line JSX/TSX in the editor or via a clean file transfer, never through `@"..."@` here-strings.
- **PowerShell `Out-File` encoding** — default UTF-8 writes a BOM and mangles emoji/em-dashes; `-Encoding ascii` plus HTML entities (`&mdash;`, `&apos;`) for display characters keeps bytes clean.
- **pnpm v11 blocks build scripts by default** — `sharp`, `unrs-resolver`, and `esbuild` need explicit `pnpm approve-builds` (a supply-chain safety default, not an error).
- **Vercel project naming** — the CLI defaults the project name to the folder (`frontend`), producing an off-brand URL. Worth setting deliberately at deploy time.

---

## Repository Structure

```
upnext/
├── frontend/              # Next.js 16 app
│   ├── app/               # App Router pages + layout
│   ├── components/
│   │   └── marketing/     # Landing page sections
│   └── lib/               # cn() utility, shared helpers
└── backend/               # FastAPI (Phase 5+)
```

---

## Roadmap

Personalization grows from simple tag-overlap filtering (V1) to vector-similarity ranking over pgvector (Phase 7), once real ingestion from GitHub, arXiv, Reddit, and Hacker News is in place. The architecture supports expansion to other professional niches later, but the MVP is focused exclusively on AI engineers.

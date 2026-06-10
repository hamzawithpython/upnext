# UpNext ? The Daily Operating System for AI Engineers

> An AI-native intelligence platform that filters, ranks, and summarizes the latest in AI engineering ? so professionals stay ahead without drowning in Twitter, Reddit, and newsletters.

## Status
?? In active development. Phase 1: landing page + design system.

## Tech Stack
- **Frontend:** Next.js 16 (App Router), TypeScript, TailwindCSS, Framer Motion, shadcn/ui
- **Backend:** FastAPI (Python 3.11)
- **Database:** PostgreSQL (Neon, with pgvector)
- **AI:** Groq (Llama 3.3 70B) ? free-tier inference
- **Deploy:** Vercel (frontend), Render (backend), Neon (DB)

## Architecture
Decoupled monolith: Next.js frontend ? FastAPI backend ? Postgres. The OpenAI-compatible AI layer runs server-side only.

## Technical Decisions
- **Groq over OpenAI:** OpenAI-SDK-compatible, zero-cost free tier ? keeps the MVP at \ without changing application code.
- **Two deployables, not microservices:** clean monolith per the no-over-engineering constraint.

## Live Demo
_Coming in Phase 1._

# UpNext — Restart & Run Guide

> How to get UpNext running locally after coming back to it. Windows + PowerShell.
> Project root: `C:\Users\Admin\Desktop\portfolio\upnext`

There are three pieces: **Backend** (FastAPI, port 8000), **Frontend** (Next.js, port 3000), and **n8n** (Docker, port 5678, for scheduled ingestion — optional). Start them in that order.

---

## 0. Prerequisites check (only if something seems broken)

```powershell
node --version      # v20+
pnpm --version
python --version    # 3.12
docker --version    # Docker Desktop must be running for n8n
```

---

## 1. Backend (FastAPI) — REQUIRED for auth, feed, assistant

Open a PowerShell window:

```powershell
cd C:\Users\Admin\Desktop\portfolio\upnext\backend
.\venv\Scripts\Activate.ps1
```

Your prompt should now show `(venv)`. If activation is blocked:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
.\venv\Scripts\Activate.ps1
```

**Port 8000 conflict check** — the Inbox Operator RAG container may be holding port 8000. If so, stop it first:

```powershell
docker stop inbox-operator-rag   # only if it's running and you don't need it now
```

Start the backend:

```powershell
uvicorn app.main:app --reload
```

Leave this window running. Verify in a browser: `http://127.0.0.1:8000/health` → should show `{"status":"ok"}`.
API docs (for manual testing): `http://127.0.0.1:8000/docs`

---

## 2. Frontend (Next.js) — REQUIRED for the UI

Open a SECOND PowerShell window:

```powershell
cd C:\Users\Admin\Desktop\portfolio\upnext\frontend
pnpm dev
```

Open `http://localhost:3000`. Log in with a test user:
- `test2@gmail.com` (has real preferences — best for testing feed/assistant)

> If you see "Failed to fetch" on the dashboard, the backend isn't running or didn't start cleanly. Check step 1. Remember: a backend 500 can masquerade as a CORS error — check the uvicorn terminal for the real traceback.

---

## 3. n8n (ingestion) — OPTIONAL, only if running/testing ingestion

n8n runs in Docker (shared with the Inbox Operator project).

```powershell
docker ps                          # is 'inbox-operator-n8n' running?
```

If not running:

```powershell
docker start inbox-operator-n8n
# or, if you use the compose file:
# cd <your n8n compose folder>; docker compose up -d
```

Wait ~15s, then open `http://localhost:5678`. The "UpNext Ingestion" workflow is there.

**Before testing ingestion:** the backend (step 1) must be running on the host, and the n8n HTTP node's `x-ingest-secret` value must match `INGEST_SECRET` in `backend\.env`. The node calls `http://host.docker.internal:8000/ingest`.

To run ingestion manually: open the workflow → "Test workflow". To run on schedule: toggle it **Active**.

---

## 4. Trigger ingestion without n8n (quick manual option)

If you just want fresh feed items and don't need n8n, hit the endpoint directly. In `/docs`:
- `POST /ingest` → set the `x-ingest-secret` header to your `INGEST_SECRET` value → body:
  ```json
  { "sources": ["hackernews", "arxiv", "github", "huggingface"], "per_source": 5 }
  ```
- Execute. Expect `{ "fetched": N, "inserted": N, "skipped_duplicates": N, "failed": 0, "errors": {} }`.

---

## Common operations

**Re-seed the initial mock feed items** (idempotent):
```powershell
cd C:\Users\Admin\Desktop\portfolio\upnext\backend
.\venv\Scripts\Activate.ps1
python -m app.seed_feed
```

**Apply new DB migrations** (after pulling changes or adding a model):
```powershell
alembic upgrade head
```

**Create a new migration** (after changing a model — remember to import the model in `alembic/env.py` first):
```powershell
alembic revision --autogenerate -m "describe change"
alembic upgrade head
```

**Inspect the DB quickly** (write a temp script, run, delete):
```powershell
@"
from app.db.session import engine
from sqlalchemy import text
with engine.connect() as conn:
    for r in conn.execute(text('SELECT source, COUNT(*) FROM feed_items GROUP BY source')):
        print(r)
"@ | Out-File -FilePath tmp_check.py -Encoding ascii
python tmp_check.py
del tmp_check.py
```

---

## Git workflow reminder

Always work on a feature branch, never directly on `main`:
```powershell
cd C:\Users\Admin\Desktop\portfolio\upnext
git checkout main
git pull origin main
git checkout -b feat/<feature-name>
# ... work, then:
git add .
git commit -m "feat: <conventional commit message>"
git push -u origin feat/<feature-name>
# when done, merge to main:
git checkout main
git merge feat/<feature-name> --no-ff -m "Merge feat/<feature-name>: <summary>"
git push origin main
```

---

## Shutting down

- Backend / Frontend: `Ctrl+C` in their windows.
- n8n: leave running, or `docker stop inbox-operator-n8n`.
- If you stopped `inbox-operator-rag` for the port and want Inbox Operator back: `docker start inbox-operator-rag` (but UpNext backend must NOT be on 8000 then, or they'll conflict).

---

## Quick reference

| Service | Command | URL |
|---|---|---|
| Backend | `uvicorn app.main:app --reload` (in backend/, venv on) | http://127.0.0.1:8000 |
| API docs | — | http://127.0.0.1:8000/docs |
| Frontend | `pnpm dev` (in frontend/) | http://localhost:3000 |
| n8n | `docker start inbox-operator-n8n` | http://localhost:5678 |

| Test user | Notes |
|---|---|
| test2@gmail.com | Real preferences — use for feed/assistant testing |

**Gotcha memory:** CORS error in browser + backend up = check uvicorn terminal for a hidden 500. Port 8000 shared with `inbox-operator-rag`. n8n reaches host via `host.docker.internal`, not `127.0.0.1`.

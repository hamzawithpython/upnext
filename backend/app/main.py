from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, feed, preferences

app = FastAPI(title="UpNext API", version="0.1.0")

# Allow the Next.js frontend (local + deployed) to call this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://frontend-one-wheat-dw5aauswjr.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(preferences.router)
app.include_router(feed.router)


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    """Liveness probe."""
    return {"status": "ok"}

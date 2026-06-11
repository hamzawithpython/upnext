from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import assistant, auth, feed, ingest, preferences

app = FastAPI(title="UpNext API", version="0.1.0")

# CORS: explicit production origin + a regex covering any localhost/127.0.0.1
# port for local dev. The regex avoids the localhost-vs-127.0.0.1 mismatch that
# blocks requests when the two are used interchangeably.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://frontend-one-wheat-dw5aauswjr.vercel.app"],
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(preferences.router)
app.include_router(feed.router)
app.include_router(assistant.router)
app.include_router(ingest.router)


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    """Liveness probe."""
    return {"status": "ok"}

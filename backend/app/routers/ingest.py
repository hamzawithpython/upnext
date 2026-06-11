from fastapi import APIRouter, Depends, Header, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.ingestion.pipeline import SOURCES, run_ingestion

router = APIRouter(prefix="/ingest", tags=["ingest"])


class IngestRequest(BaseModel):
    sources: list[str] = []
    per_source: int = 8


def verify_ingest_secret(x_ingest_secret: str = Header(default="")) -> None:
    """Machine-to-machine auth for the ingestion trigger (n8n sends this header)."""
    if x_ingest_secret != settings.INGEST_SECRET:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid ingest secret.",
        )


@router.get("/sources")
def list_sources() -> dict:
    """List available ingestion sources (handy for debugging)."""
    return {"sources": list(SOURCES.keys())}


@router.post("", dependencies=[Depends(verify_ingest_secret)])
def ingest(payload: IngestRequest, db: Session = Depends(get_db)) -> dict:
    """Run ingestion for the requested sources (or all if none given)."""
    return run_ingestion(db, payload.sources, payload.per_source)

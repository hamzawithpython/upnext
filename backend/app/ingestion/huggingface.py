"""HuggingFace source. Uses a read token.

Pulls recently-trending models from the HF Hub API. Skips gracefully if no
token is configured.
"""

from datetime import datetime, timezone

import httpx

from app.core.config import settings
from app.ingestion.types import RawItem

_API = "https://huggingface.co/api/models"


def fetch_huggingface(limit: int = 8) -> list[RawItem]:
    if not settings.HF_TOKEN:
        return []

    params = {
        "sort": "trendingScore",
        "direction": "-1",
        "limit": str(limit),
        "full": "true",
    }
    headers = {"Authorization": f"Bearer {settings.HF_TOKEN}"}
    with httpx.Client(timeout=20) as client:
        resp = client.get(_API, params=params, headers=headers)
        resp.raise_for_status()
        data = resp.json()

    items: list[RawItem] = []
    for model in data[:limit]:
        model_id = model.get("id") or model.get("modelId", "")
        if not model_id:
            continue
        created_raw = model.get("createdAt", "")
        try:
            published = datetime.fromisoformat(created_raw.replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            published = datetime.now(timezone.utc)

        pipeline_tag = model.get("pipeline_tag", "")
        downloads = model.get("downloads", 0)

        items.append(
            RawItem(
                external_id=model_id,
                source="huggingface",
                title=f"Trending model: {model_id}",
                url=f"https://huggingface.co/{model_id}",
                raw_content=(
                    f"HuggingFace model {model_id}. Task: {pipeline_tag or 'unspecified'}. "
                    f"{downloads} downloads."
                ),
                published_at=published,
                seed_tags=[pipeline_tag] if pipeline_tag else [],
            )
        )
    return items

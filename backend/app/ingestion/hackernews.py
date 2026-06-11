"""Hacker News source. No auth required.

Pulls top stories from the Firebase API, keeps those that look AI/ML-relevant
by a simple keyword filter on the title.
"""

from datetime import datetime, timezone

import httpx

from app.ingestion.types import RawItem

_TOP_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
_ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{id}.json"

_KEYWORDS = (
    "ai", "llm", "gpt", "agent", "rag", "embedding", "ml ", "machine learning",
    "neural", "model", "openai", "anthropic", "langchain", "vector", "fine-tune",
    "fine tune", "transformer", "inference", "groq", "llama", "mistral", "diffusion",
)


def _is_relevant(title: str) -> bool:
    t = title.lower()
    return any(k in t for k in _KEYWORDS)


def fetch_hackernews(limit: int = 10) -> list[RawItem]:
    items: list[RawItem] = []
    with httpx.Client(timeout=20) as client:
        top_ids = client.get(_TOP_URL).json()[:80]
        for story_id in top_ids:
            if len(items) >= limit:
                break
            data = client.get(_ITEM_URL.format(id=story_id)).json()
            if not data or data.get("type") != "story":
                continue
            title = data.get("title", "")
            if not _is_relevant(title):
                continue
            url = data.get("url") or f"https://news.ycombinator.com/item?id={story_id}"
            published = datetime.fromtimestamp(
                data.get("time", 0), tz=timezone.utc
            )
            items.append(
                RawItem(
                    external_id=str(story_id),
                    source="hackernews",
                    title=title,
                    url=url,
                    raw_content=f"{title}\n\nDiscussion on Hacker News with {data.get('score', 0)} points and {data.get('descendants', 0)} comments.",
                    published_at=published,
                    seed_tags=[],
                )
            )
    return items

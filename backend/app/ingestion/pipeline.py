"""Ingestion pipeline orchestrator.

Given a list of source names, fetches RawItems, drops ones already in the DB,
summarizes the new ones with Groq, and inserts them into feed_items.

Each item is processed in isolation: a failure on one item (network, DB, or
model) is recorded and skipped rather than aborting the whole run. A source
with no configured credentials simply returns nothing and is skipped.
"""

import time

from sqlalchemy.orm import Session

from app.ingestion.arxiv import fetch_arxiv
from app.ingestion.github import fetch_github
from app.ingestion.hackernews import fetch_hackernews
from app.ingestion.huggingface import fetch_huggingface
from app.ingestion.types import RawItem
from app.models.feed_item import FeedItemModel
from app.services.groq_service import generate_summary

# Registry: source name -> fetcher function. Add sources here.
SOURCES = {
    "hackernews": fetch_hackernews,
    "arxiv": fetch_arxiv,
    "github": fetch_github,
    "huggingface": fetch_huggingface,
}


def _make_feed_id(item: RawItem) -> str:
    return item.dedup_key.replace("/", "_")[:200]


def run_ingestion(db: Session, sources: list[str], per_source: int = 8) -> dict:
    requested = sources or list(SOURCES.keys())

    fetched: list[RawItem] = []
    errors: dict[str, str] = {}
    for name in requested:
        fetcher = SOURCES.get(name)
        if not fetcher:
            errors[name] = "unknown source"
            continue
        try:
            fetched.extend(fetcher(limit=per_source))
        except Exception as exc:  # noqa: BLE001
            errors[name] = f"fetch failed: {exc}"

    inserted = 0
    skipped = 0
    failed = 0
    for item in fetched:
        feed_id = _make_feed_id(item)
        if db.get(FeedItemModel, feed_id) is not None:
            skipped += 1
            continue

        try:
            summary = generate_summary(item.title, item.raw_content, item.source)
            tags = list(summary["tags"])
            for t in item.seed_tags:
                if t not in tags:
                    tags.append(t)

            db.add(
                FeedItemModel(
                    id=feed_id,
                    source=item.source,
                    title=item.title,
                    url=item.url,
                    summary=summary["summary"],
                    why_matters=summary["why_matters"],
                    impact=summary["impact"],
                    tags=tags[:6],
                    published_at=item.published_at,
                )
            )
            db.commit()
            inserted += 1
        except Exception as exc:  # noqa: BLE001 - isolate per-item failures
            db.rollback()
            failed += 1
            errors[item.dedup_key] = str(exc)

        time.sleep(1.2)  # pace Groq free-tier

    return {
        "fetched": len(fetched),
        "inserted": inserted,
        "skipped_duplicates": skipped,
        "failed": failed,
        "errors": errors,
    }

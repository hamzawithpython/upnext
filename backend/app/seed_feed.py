"""Seed the feed_items table from the mock data set.

Idempotent: upserts by id, so running it repeatedly won't create duplicates.

Usage (from backend/, venv active):  python -m app.seed_feed
"""

from datetime import datetime

from app.data.mock_feed import MOCK_FEED
from app.db.session import SessionLocal
from app.models.feed_item import FeedItemModel


def seed() -> None:
    db = SessionLocal()
    try:
        inserted = 0
        updated = 0
        for item in MOCK_FEED:
            published_at = datetime.fromisoformat(item["published_at"])
            existing = db.get(FeedItemModel, item["id"])
            if existing is None:
                db.add(
                    FeedItemModel(
                        id=item["id"],
                        source=item["source"],
                        title=item["title"],
                        url=item["url"],
                        summary=item["summary"],
                        why_matters=item["why_matters"],
                        impact=item["impact"],
                        tags=item["tags"],
                        published_at=published_at,
                    )
                )
                inserted += 1
            else:
                existing.source = item["source"]
                existing.title = item["title"]
                existing.url = item["url"]
                existing.summary = item["summary"]
                existing.why_matters = item["why_matters"]
                existing.impact = item["impact"]
                existing.tags = item["tags"]
                existing.published_at = published_at
                updated += 1

        db.commit()
        print(f"Seed complete. Inserted {inserted}, updated {updated}.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()

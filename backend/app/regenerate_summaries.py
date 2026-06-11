"""Regenerate feed-item summaries with Groq.

For each feed_items row, calls the Groq service to (re)generate
summary / why_matters / impact / tags, then writes them back to the DB.

Phase 6 note: the mock items have no separate raw article body, so we feed the
model the existing title + summary as source text. In Phase 7, real ingestion
supplies full article content and this same script produces grounded summaries
from that. The pipeline shape is identical; only the input source changes.

Usage (from backend/, venv active):  python -m app.regenerate_summaries
"""

import time

from app.db.session import SessionLocal
from app.models.feed_item import FeedItemModel
from app.services.groq_service import generate_summary


def run() -> None:
    db = SessionLocal()
    try:
        rows = db.query(FeedItemModel).order_by(FeedItemModel.id).all()
        print(f"Regenerating summaries for {len(rows)} items...\n")

        for row in rows:
            source_text = f"{row.title}\n\n{row.summary}"
            result = generate_summary(
                title=row.title,
                raw_content=source_text,
                source=row.source,
            )

            row.summary = result["summary"]
            row.why_matters = result["why_matters"]
            row.impact = result["impact"]
            # Merge AI tags with existing tags, dedup, cap at 6, preserve order.
            merged: list[str] = []
            for t in [*row.tags, *result["tags"]]:
                if t not in merged:
                    merged.append(t)
            row.tags = merged[:6]

            db.commit()
            print(f"  {row.id}: {result['impact']:6} | {row.title[:50]}")

            # Gentle pacing to stay under the free-tier rate limit.
            time.sleep(1.5)

        print("\nDone. All summaries regenerated.")
    finally:
        db.close()


if __name__ == "__main__":
    run()

"""arXiv source. No auth required.

Queries the arXiv Atom API for recent papers in AI-relevant categories
(cs.AI, cs.CL, cs.LG) and maps them to RawItems.
"""

from datetime import datetime, timezone
from xml.etree import ElementTree as ET

import httpx

from app.ingestion.types import RawItem

# arXiv now requires https; follow_redirects handles the http->https 301.
_API = "https://export.arxiv.org/api/query"
_ATOM = "{http://www.w3.org/2005/Atom}"


def fetch_arxiv(limit: int = 8) -> list[RawItem]:
    params = {
        "search_query": "cat:cs.AI OR cat:cs.CL OR cat:cs.LG",
        "sortBy": "submittedDate",
        "sortOrder": "descending",
        "max_results": str(limit),
    }
    with httpx.Client(timeout=20, follow_redirects=True) as client:
        resp = client.get(_API, params=params)
        resp.raise_for_status()
        root = ET.fromstring(resp.text)

    items: list[RawItem] = []
    for entry in root.findall(f"{_ATOM}entry"):
        arxiv_url = entry.findtext(f"{_ATOM}id", default="").strip()
        external_id = arxiv_url.rsplit("/", 1)[-1] if arxiv_url else ""
        title = " ".join(entry.findtext(f"{_ATOM}title", default="").split())
        summary_text = " ".join(
            entry.findtext(f"{_ATOM}summary", default="").split()
        )
        published_raw = entry.findtext(f"{_ATOM}published", default="")
        try:
            published = datetime.fromisoformat(published_raw.replace("Z", "+00:00"))
        except ValueError:
            published = datetime.now(timezone.utc)

        if not external_id or not title:
            continue

        items.append(
            RawItem(
                external_id=external_id,
                source="arxiv",
                title=title,
                url=arxiv_url,
                raw_content=f"{title}\n\nAbstract: {summary_text}",
                published_at=published,
                seed_tags=[],
            )
        )
    return items

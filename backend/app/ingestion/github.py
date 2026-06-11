"""GitHub source. Uses a personal access token.

Searches recently-pushed AI/LLM repos sorted by stars, as a proxy for
'trending'. Skips gracefully if no token is configured.
"""

from datetime import datetime, timedelta, timezone

import httpx

from app.core.config import settings
from app.ingestion.types import RawItem

_API = "https://api.github.com/search/repositories"


def fetch_github(limit: int = 8) -> list[RawItem]:
    if not settings.GITHUB_TOKEN:
        return []

    since = (datetime.now(timezone.utc) - timedelta(days=30)).strftime("%Y-%m-%d")
    # Valid GitHub search syntax: a free-text term plus qualifiers. Parenthesized
    # OR of topics is what triggered the 422; a single language/keyword query with
    # a pushed-date floor is valid and returns active AI repos.
    query = f"LLM agent pushed:>{since} stars:>50"
    params = {
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": str(limit),
    }
    headers = {
        "Authorization": f"Bearer {settings.GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    with httpx.Client(timeout=20) as client:
        resp = client.get(_API, params=params, headers=headers)
        resp.raise_for_status()
        data = resp.json()

    items: list[RawItem] = []
    for repo in data.get("items", [])[:limit]:
        full_name = repo.get("full_name", "")
        description = repo.get("description") or ""
        created_raw = repo.get("created_at", "")
        try:
            published = datetime.fromisoformat(created_raw.replace("Z", "+00:00"))
        except ValueError:
            published = datetime.now(timezone.utc)

        if not full_name:
            continue

        items.append(
            RawItem(
                external_id=str(repo.get("id", full_name)),
                source="github",
                title=full_name,
                url=repo.get("html_url", ""),
                raw_content=(
                    f"GitHub repository {full_name} "
                    f"({repo.get('stargazers_count', 0)} stars). {description}"
                ),
                published_at=published,
                seed_tags=list(repo.get("topics", []))[:3],
            )
        )
    return items

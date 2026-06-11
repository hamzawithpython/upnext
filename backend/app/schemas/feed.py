from datetime import datetime
from typing import Literal

from pydantic import BaseModel

Impact = Literal["low", "medium", "high"]
Source = Literal[
    "github",
    "arxiv",
    "reddit",
    "hackernews",
    "huggingface",
    "news",
    "producthunt",
]


class FeedItem(BaseModel):
    """A single ranked, summarized feed item.

    In Phase 4 these come from a static mock set. In Phase 5+ they are served
    from Postgres; in Phase 6 the summary/why_matters are AI-generated and in
    Phase 7 they are ingested from real sources. The shape stays constant.
    """

    id: str
    source: Source
    title: str
    url: str
    summary: str
    why_matters: str
    impact: Impact
    tags: list[str]
    published_at: datetime


class FeedResponse(BaseModel):
    items: list[FeedItem]
    total: int
    personalized: bool

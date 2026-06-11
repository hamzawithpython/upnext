"""Shared types for ingestion sources.

Each source fetcher returns a list of RawItem. The pipeline then normalizes,
dedups, summarizes (Groq), and stores them. Adding a source means writing one
function that returns RawItem objects — nothing else in the pipeline changes.
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class RawItem:
    """A source-agnostic item before AI summarization.

    external_id makes dedup deterministic: the same HN story or GitHub repo
    won't be inserted twice across runs.
    """

    external_id: str
    source: str
    title: str
    url: str
    raw_content: str
    published_at: datetime
    seed_tags: list[str] = field(default_factory=list)

    @property
    def dedup_key(self) -> str:
        return f"{self.source}:{self.external_id}"

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.data.mock_feed import MOCK_FEED
from app.db.session import get_db
from app.deps import get_current_user
from app.models.preferences import UserPreferences
from app.models.user import User
from app.schemas.feed import FeedItem, FeedResponse

router = APIRouter(prefix="/feed", tags=["feed"])

_IMPACT_RANK = {"high": 3, "medium": 2, "low": 1}


@router.get("", response_model=FeedResponse)
def get_feed(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> FeedResponse:
    """Return a personalized feed.

    Phase 4: ranks a static mock set against the user's interests/tools.
    Items matching more of the user's tags rank higher; ties break on impact
    then recency. If the user has no preferences yet, returns the full set
    ranked by impact + recency (personalized=False).
    """
    prefs = (
        db.query(UserPreferences)
        .filter(UserPreferences.user_id == current_user.id)
        .first()
    )

    user_tags: set[str] = set()
    if prefs:
        user_tags = {t.lower() for t in (prefs.interests + prefs.tools)}

    items = [FeedItem(**item) for item in MOCK_FEED]

    def score(item: FeedItem) -> tuple[int, int, str]:
        overlap = len({t.lower() for t in item.tags} & user_tags)
        return (overlap, _IMPACT_RANK[item.impact], item.published_at.isoformat())

    items.sort(key=score, reverse=True)

    return FeedResponse(
        items=items,
        total=len(items),
        personalized=bool(user_tags),
    )

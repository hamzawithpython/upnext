from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.deps import get_current_user
from app.models.preferences import UserPreferences
from app.models.user import User
from app.schemas.preferences import PreferencesOut, PreferencesUpdate

router = APIRouter(prefix="/preferences", tags=["preferences"])


def _get_or_create(db: Session, user_id) -> UserPreferences:
    prefs = (
        db.query(UserPreferences)
        .filter(UserPreferences.user_id == user_id)
        .first()
    )
    if prefs is None:
        prefs = UserPreferences(user_id=user_id)
        db.add(prefs)
        db.commit()
        db.refresh(prefs)
    return prefs


@router.get("", response_model=PreferencesOut)
def get_preferences(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> UserPreferences:
    """Return the current user's preferences, creating an empty row if needed.

    The `onboarded` flag tells the frontend whether to route to onboarding.
    """
    return _get_or_create(db, current_user.id)


@router.put("", response_model=PreferencesOut)
def update_preferences(
    payload: PreferencesUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> UserPreferences:
    """Save onboarding preferences and mark the user as onboarded."""
    prefs = _get_or_create(db, current_user.id)

    prefs.skill_level = payload.skill_level
    prefs.interests = payload.interests
    prefs.tools = payload.tools
    prefs.goals = payload.goals
    prefs.content_style = payload.content_style
    prefs.onboarded = True

    db.commit()
    db.refresh(prefs)
    return prefs

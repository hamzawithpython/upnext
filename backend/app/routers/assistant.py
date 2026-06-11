from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.deps import get_current_user
from app.models.preferences import UserPreferences
from app.models.user import User
from app.schemas.chat import ChatRequest
from app.services.groq_service import stream_chat

router = APIRouter(prefix="/assistant", tags=["assistant"])


def _build_system_prompt(prefs: UserPreferences | None) -> str:
    base = (
        "You are UpNext's AI assistant, helping AI engineers stay current and "
        "learn faster. Be concise, concrete, and practical. When asked what to "
        "learn next, give specific, actionable suggestions. Avoid hype."
    )
    if not prefs:
        return base

    context_parts = []
    if prefs.skill_level:
        context_parts.append(f"skill level: {prefs.skill_level}")
    if prefs.interests:
        context_parts.append(f"interests: {', '.join(prefs.interests)}")
    if prefs.tools:
        context_parts.append(f"tools they use: {', '.join(prefs.tools)}")
    if prefs.goals:
        context_parts.append(f"goals: {', '.join(prefs.goals)}")
    if prefs.content_style:
        context_parts.append(f"preferred style: {prefs.content_style}")

    if context_parts:
        return base + "\n\nAbout this user — " + "; ".join(context_parts) + "."
    return base


@router.post("")
def chat(
    payload: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> StreamingResponse:
    """Stream an assistant reply, grounded in the user's preferences."""
    prefs = (
        db.query(UserPreferences)
        .filter(UserPreferences.user_id == current_user.id)
        .first()
    )
    system_prompt = _build_system_prompt(prefs)

    messages = [{"role": m.role, "content": m.content} for m in payload.messages]

    def event_stream():
        for chunk in stream_chat(messages, system_prompt):
            yield chunk

    return StreamingResponse(event_stream(), media_type="text/plain")

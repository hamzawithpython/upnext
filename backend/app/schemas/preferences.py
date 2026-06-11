import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PreferencesUpdate(BaseModel):
    """Request body for saving onboarding preferences."""

    skill_level: str | None = Field(default=None)
    interests: list[str] = Field(default_factory=list)
    tools: list[str] = Field(default_factory=list)
    goals: list[str] = Field(default_factory=list)
    content_style: str | None = Field(default=None)


class PreferencesOut(BaseModel):
    """Preferences as returned to the client."""

    user_id: uuid.UUID
    skill_level: str | None
    interests: list[str]
    tools: list[str]
    goals: list[str]
    content_style: str | None
    onboarded: bool
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

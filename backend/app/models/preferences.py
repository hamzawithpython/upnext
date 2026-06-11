import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class UserPreferences(Base):
    __tablename__ = "user_preferences"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    skill_level: Mapped[str | None] = mapped_column(String, nullable=True)
    interests: Mapped[list[str]] = mapped_column(
        ARRAY(String), nullable=False, default=list
    )
    tools: Mapped[list[str]] = mapped_column(
        ARRAY(String), nullable=False, default=list
    )
    goals: Mapped[list[str]] = mapped_column(
        ARRAY(String), nullable=False, default=list
    )
    content_style: Mapped[str | None] = mapped_column(String, nullable=True)
    onboarded: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

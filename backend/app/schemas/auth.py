import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    """Request body for signup."""

    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserLogin(BaseModel):
    """Request body for login."""

    email: EmailStr
    password: str


class UserOut(BaseModel):
    """Public user representation (never includes the password hash)."""

    id: uuid.UUID
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    """JWT response returned on signup/login."""

    access_token: str
    token_type: str = "bearer"

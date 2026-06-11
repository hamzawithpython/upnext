from typing import Literal

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=4000)


class ChatRequest(BaseModel):
    """Running conversation sent from the chat panel."""

    messages: list[ChatMessage] = Field(min_length=1, max_length=40)

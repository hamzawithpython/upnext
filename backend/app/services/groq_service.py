"""Groq LLM service.

Wraps the Groq client for two uses:
  1. Generating feed-item summaries (structured JSON).
  2. Powering the assistant chat (streaming).

Groq is OpenAI-API-compatible; the official `groq` SDK is used here. The model
is configurable via GROQ_MODEL so a deprecation only requires an env change.
"""

import json
from collections.abc import Iterator

from groq import Groq

from app.core.config import settings

_client = Groq(api_key=settings.GROQ_API_KEY)

VALID_IMPACTS = {"low", "medium", "high"}


def generate_summary(title: str, raw_content: str, source: str) -> dict:
    """Generate a structured summary for a feed item.

    Returns a dict with keys: summary, why_matters, impact, tags.
    Falls back to safe defaults if the model returns malformed JSON.
    """
    system = (
        "You are an editor for an intelligence feed read by AI engineers. "
        "Given a title and content, produce a tight, factual briefing. "
        "Respond ONLY with a JSON object, no markdown, no preamble, with keys: "
        '"summary" (2 sentences max, plain and concrete), '
        '"why_matters" (1 sentence on why an AI engineer should care), '
        '"impact" (one of "low", "medium", "high"), '
        '"tags" (3-5 short topic tags as a JSON array of strings). '
        "Do not invent facts not present in the content."
    )
    user = f"Source: {source}\nTitle: {title}\n\nContent:\n{raw_content}"

    completion = _client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=0.3,
        response_format={"type": "json_object"},
    )

    content = completion.choices[0].message.content or "{}"
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        data = {}

    impact = str(data.get("impact", "medium")).lower()
    if impact not in VALID_IMPACTS:
        impact = "medium"

    tags = data.get("tags", [])
    if not isinstance(tags, list):
        tags = []

    return {
        "summary": str(data.get("summary", "")).strip() or "Summary unavailable.",
        "why_matters": str(data.get("why_matters", "")).strip()
        or "Relevance pending.",
        "impact": impact,
        "tags": [str(t) for t in tags][:5],
    }


def stream_chat(messages: list[dict], system_prompt: str) -> Iterator[str]:
    """Stream an assistant chat completion as text chunks.

    `messages` is the running conversation [{role, content}, ...].
    Yields content deltas as they arrive.
    """
    full_messages = [{"role": "system", "content": system_prompt}, *messages]

    stream = _client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=full_messages,
        temperature=0.5,
        stream=True,
    )

    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta

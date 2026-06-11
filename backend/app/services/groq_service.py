"""Groq LLM service.

Wraps the Groq client for two uses:
  1. Generating feed-item summaries (structured JSON, resilient to bad output).
  2. Powering the assistant chat (streaming).

Groq is OpenAI-API-compatible; the official `groq` SDK is used here. The model
is configurable via GROQ_MODEL so a deprecation only requires an env change.
"""

import json
from collections.abc import Iterator

from groq import BadRequestError, Groq

from app.core.config import settings

_client = Groq(api_key=settings.GROQ_API_KEY)

VALID_IMPACTS = {"low", "medium", "high"}


def _coerce(data: dict) -> dict:
    """Normalize a parsed model response into our summary shape."""
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


def _fallback(title: str) -> dict:
    """Safe summary used when the model can't produce valid JSON."""
    return {
        "summary": title.strip()[:300] or "Summary unavailable.",
        "why_matters": "Flagged as potentially relevant to AI engineering.",
        "impact": "low",
        "tags": [],
    }


def generate_summary(title: str, raw_content: str, source: str) -> dict:
    """Generate a structured summary for a feed item.

    Resilient by design: retries once on malformed JSON, and falls back to a
    safe non-AI summary rather than raising — so a single bad item never crashes
    a batch ingestion run.
    """
    system = (
        "You are an editor for an intelligence feed read by AI engineers. "
        "Given a title and content, produce a tight, factual briefing. "
        "Respond ONLY with a valid JSON object. Every string value MUST be "
        "wrapped in double quotes. No markdown, no preamble. Keys: "
        '"summary" (2 sentences max), "why_matters" (1 sentence), '
        '"impact" (exactly one of "low", "medium", "high"), '
        '"tags" (3-5 short strings as a JSON array). '
        "Do not invent facts not present in the content."
    )
    user = f"Source: {source}\nTitle: {title}\n\nContent:\n{raw_content}"
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]

    for attempt in range(2):
        try:
            completion = _client.chat.completions.create(
                model=settings.GROQ_MODEL,
                messages=messages,
                temperature=0.2 if attempt == 0 else 0.0,
                response_format={"type": "json_object"},
            )
            content = completion.choices[0].message.content or "{}"
            return _coerce(json.loads(content))
        except (json.JSONDecodeError, BadRequestError):
            # Bad JSON from the model. Retry once at temp 0; then fall back.
            continue

    return _fallback(title)


def stream_chat(messages: list[dict], system_prompt: str) -> Iterator[str]:
    """Stream an assistant chat completion as text chunks."""
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

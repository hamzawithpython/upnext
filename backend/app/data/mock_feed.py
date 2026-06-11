"""Static mock feed data for Phase 4.

Each item mimics what the real ingestion + AI-summary pipeline will produce in
later phases. Tags align with the onboarding vocabulary in
frontend/lib/onboarding-options.ts so personalization filtering works.
"""

from datetime import datetime, timedelta, timezone

_now = datetime.now(timezone.utc)


def _ago(hours: int) -> str:
    return (_now - timedelta(hours=hours)).isoformat()


MOCK_FEED: list[dict] = [
    {
        "id": "feed_001",
        "source": "github",
        "title": "LangGraph 1.0 ships durable execution and built-in checkpointing",
        "url": "https://github.com/langchain-ai/langgraph",
        "summary": "LangGraph's 1.0 release stabilizes the state-graph API and adds durable execution, letting long-running agent workflows resume after failures without losing state.",
        "why_matters": "If you build multi-agent systems, durable execution removes a major reliability gap — agents can now survive restarts mid-run.",
        "impact": "high",
        "tags": ["AI Agents", "LangChain", "LangGraph"],
        "published_at": _ago(3),
    },
    {
        "id": "feed_002",
        "source": "arxiv",
        "title": "Late-interaction retrieval beats dense embeddings on long-document RAG",
        "url": "https://arxiv.org/abs/2410.00000",
        "summary": "A new paper benchmarks ColBERT-style late-interaction retrieval against dense single-vector embeddings, showing consistent gains on long-document question answering.",
        "why_matters": "For RAG over long documents, switching retrieval strategy may beat swapping to a bigger embedding model — cheaper and more accurate.",
        "impact": "medium",
        "tags": ["RAG", "Vector Databases"],
        "published_at": _ago(8),
    },
    {
        "id": "feed_003",
        "source": "news",
        "title": "Groq announces lower free-tier rate limits for open models",
        "url": "https://groq.com/blog",
        "summary": "Groq updated its free-tier pricing and rate limits for hosted open-weight models, adjusting requests-per-day caps for several Llama variants.",
        "why_matters": "If you prototype on Groq's free tier, the new caps may affect how you architect batching and caching for demos.",
        "impact": "medium",
        "tags": ["OpenAI", "Local LLMs", "Automation"],
        "published_at": _ago(12),
    },
    {
        "id": "feed_004",
        "source": "reddit",
        "title": "Discussion: when does MCP actually beat a plain function-calling setup?",
        "url": "https://reddit.com/r/LocalLLaMA",
        "summary": "A widely-upvoted thread debates where the Model Context Protocol adds value over direct tool/function calling, with practitioners sharing where the abstraction pays off versus adds overhead.",
        "why_matters": "Useful gut-check before adopting MCP — the consensus is it shines for reusable, cross-app tool servers, less so for single-app tools.",
        "impact": "low",
        "tags": ["MCP", "AI Agents"],
        "published_at": _ago(18),
    },
    {
        "id": "feed_005",
        "source": "github",
        "title": "n8n adds native vector store nodes for RAG workflows",
        "url": "https://github.com/n8n-io/n8n",
        "summary": "n8n's latest release introduces first-class vector store nodes, letting you build retrieval-augmented automation flows without external glue code.",
        "why_matters": "For automation builders, RAG pipelines can now live entirely inside n8n — fewer moving parts for support-bot and triage workflows.",
        "impact": "high",
        "tags": ["n8n", "Automation", "RAG", "Vector Databases"],
        "published_at": _ago(20),
    },
    {
        "id": "feed_006",
        "source": "producthunt",
        "title": "New open-source framework for evaluating agent tool-use accuracy",
        "url": "https://producthunt.com",
        "summary": "A launch introduces an open-source eval harness focused specifically on measuring whether agents call the right tools with the right arguments.",
        "why_matters": "Agent eval is still immature; a focused tool-use benchmark helps you catch regressions before they hit production.",
        "impact": "medium",
        "tags": ["AI Agents", "LangChain", "Fine-tuning"],
        "published_at": _ago(26),
    },
    {
        "id": "feed_007",
        "source": "arxiv",
        "title": "Small fine-tuned models match large ones on narrow automation tasks",
        "url": "https://arxiv.org/abs/2410.11111",
        "summary": "Research shows that for narrow, well-defined automation tasks, a small fine-tuned model can match a much larger general model at a fraction of the inference cost.",
        "why_matters": "For high-volume automation, fine-tuning a small model may cut your inference bill dramatically without quality loss.",
        "impact": "high",
        "tags": ["Fine-tuning", "Automation", "Local LLMs"],
        "published_at": _ago(30),
    },
    {
        "id": "feed_008",
        "source": "hackernews",
        "title": "Show HN: I built a local-first RAG setup with Chroma and Ollama",
        "url": "https://news.ycombinator.com",
        "summary": "A developer shares a fully local RAG stack combining Chroma for vector storage and Ollama for inference, with no cloud dependencies.",
        "why_matters": "A practical reference if you want a privacy-preserving, zero-API-cost RAG setup for sensitive data.",
        "impact": "low",
        "tags": ["RAG", "Local LLMs", "Vector Databases", "Chroma"],
        "published_at": _ago(34),
    },
    {
        "id": "feed_009",
        "source": "news",
        "title": "OpenAI ships structured outputs guarantee for function calling",
        "url": "https://openai.com/blog",
        "summary": "OpenAI's API now guarantees schema-conformant structured outputs for function calling, eliminating a class of parsing errors in agent pipelines.",
        "why_matters": "If you parse model outputs into typed objects, this removes brittle retry logic — the schema is enforced server-side.",
        "impact": "high",
        "tags": ["OpenAI", "AI Agents", "LangChain"],
        "published_at": _ago(40),
    },
    {
        "id": "feed_010",
        "source": "github",
        "title": "FastAPI 0.118 adds first-class background task groups",
        "url": "https://github.com/fastapi/fastapi",
        "summary": "FastAPI's latest version improves background task handling with structured task groups, useful for fire-and-forget work after a response.",
        "why_matters": "Cleaner pattern for kicking off ingestion or embedding jobs after an API call without blocking the response.",
        "impact": "low",
        "tags": ["FastAPI", "Automation"],
        "published_at": _ago(46),
    },
]

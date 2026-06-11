// Fixed option sets for onboarding. Kept in one place so the feed/personalization
// logic in later phases can reference the same vocabulary.

export const SKILL_LEVELS = [
  { value: "beginner", label: "Beginner", desc: "New to AI engineering" },
  { value: "intermediate", label: "Intermediate", desc: "Shipping real projects" },
  { value: "advanced", label: "Advanced", desc: "Deep production experience" },
];

export const INTERESTS = [
  "AI Agents",
  "RAG",
  "MCP",
  "OpenAI",
  "LangChain",
  "n8n",
  "Local LLMs",
  "Automation",
  "Vector Databases",
  "AI Startups",
  "Fine-tuning",
  "Computer Vision",
];

export const TOOLS = [
  "LangChain",
  "LangGraph",
  "LlamaIndex",
  "n8n",
  "Make.com",
  "OpenAI API",
  "Groq",
  "Chroma",
  "Pinecone",
  "FastAPI",
  "Docker",
  "Hugging Face",
];

export const GOALS = [
  "Stay current daily",
  "Learn faster",
  "Ship side projects",
  "Find tools to adopt",
  "Track research",
  "Land a job / clients",
];

export const CONTENT_STYLES = [
  { value: "concise", label: "Concise", desc: "Quick hits, minimal reading" },
  { value: "deep", label: "In-depth", desc: "Full context and detail" },
];

// Thin API client for the UpNext backend.
// Token is stored in localStorage for the MVP. Known tradeoff: localStorage is
// readable by XSS. A production hardening would move to httpOnly cookies +
// middleware-based route protection. Documented in the README security section.

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

const TOKEN_KEY = "upnext_token";

export function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem(TOKEN_KEY);
}

export function setToken(token: string): void {
  localStorage.setItem(TOKEN_KEY, token);
}

export function clearToken(): void {
  localStorage.removeItem(TOKEN_KEY);
}

type AuthResponse = { access_token: string; token_type: string };

type ApiError = { detail: string };

async function postJson<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    let message = "Something went wrong. Please try again.";
    try {
      const err = (await res.json()) as ApiError;
      if (err.detail) message = err.detail;
    } catch {
      // response had no JSON body; keep the default message
    }
    throw new Error(message);
  }

  return (await res.json()) as T;
}

export async function signup(email: string, password: string): Promise<void> {
  const data = await postJson<AuthResponse>("/auth/signup", { email, password });
  setToken(data.access_token);
}

export async function login(email: string, password: string): Promise<void> {
  const data = await postJson<AuthResponse>("/auth/login", { email, password });
  setToken(data.access_token);
}

export type CurrentUser = { id: string; email: string; created_at: string };

export async function getCurrentUser(): Promise<CurrentUser | null> {
  const token = getToken();
  if (!token) return null;

  const res = await fetch(`${API_URL}/auth/me`, {
    headers: { Authorization: `Bearer ${token}` },
  });

  if (!res.ok) {
    clearToken();
    return null;
  }

  return (await res.json()) as CurrentUser;
}

async function authedFetch(path: string, init?: RequestInit): Promise<Response> {
  const token = getToken();
  return fetch(`${API_URL}${path}`, {
    ...init,
    headers: {
      ...(init?.headers ?? {}),
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
  });
}

// --- Preferences ---

export type Preferences = {
  user_id: string;
  skill_level: string | null;
  interests: string[];
  tools: string[];
  goals: string[];
  content_style: string | null;
  onboarded: boolean;
  updated_at: string;
};

export type PreferencesInput = {
  skill_level: string | null;
  interests: string[];
  tools: string[];
  goals: string[];
  content_style: string | null;
};

export async function getPreferences(): Promise<Preferences | null> {
  const res = await authedFetch("/preferences");
  if (!res.ok) return null;
  return (await res.json()) as Preferences;
}

export async function savePreferences(
  input: PreferencesInput
): Promise<Preferences> {
  const res = await authedFetch("/preferences", {
    method: "PUT",
    body: JSON.stringify(input),
  });
  if (!res.ok) {
    throw new Error("Failed to save preferences. Please try again.");
  }
  return (await res.json()) as Preferences;
}

// --- Feed ---

export type Impact = "low" | "medium" | "high";

export type FeedItem = {
  id: string;
  source: string;
  title: string;
  url: string;
  summary: string;
  why_matters: string;
  impact: Impact;
  tags: string[];
  published_at: string;
};

export type FeedResponse = {
  items: FeedItem[];
  total: number;
  personalized: boolean;
};

export async function getFeed(): Promise<FeedResponse | null> {
  const res = await authedFetch("/feed");
  if (!res.ok) return null;
  return (await res.json()) as FeedResponse;
}

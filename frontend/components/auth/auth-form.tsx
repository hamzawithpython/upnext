"use client";

import { motion } from "framer-motion";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";

import { getPreferences } from "@/lib/api";

type AuthFormProps = {
  mode: "login" | "signup";
  action: (email: string, password: string) => Promise<void>;
};

export function AuthForm({ mode, action }: AuthFormProps) {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const isSignup = mode === "signup";

  const handleSubmit = async () => {
    setError(null);

    if (!email.includes("@")) {
      setError("Please enter a valid email.");
      return;
    }
    if (isSignup && password.length < 8) {
      setError("Password must be at least 8 characters.");
      return;
    }

    setLoading(true);
    try {
      await action(email, password);
      // Route based on onboarding status: new users onboard first.
      const prefs = await getPreferences();
      router.push(prefs?.onboarded ? "/dashboard" : "/onboarding");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="relative flex min-h-screen items-center justify-center px-6">
      <div className="glow left-1/2 top-1/2 h-64 w-64 -translate-x-1/2 -translate-y-1/2 bg-brand" />
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="glass relative z-10 w-full max-w-md rounded-3xl p-10"
      >
        <h1 className="text-3xl font-bold tracking-tight">
          {isSignup ? "Create your account" : "Welcome back"}
        </h1>
        <p className="mt-2 text-sm text-fg-muted">
          {isSignup
            ? "Join the AI engineers staying ahead with UpNext."
            : "Sign in to your UpNext dashboard."}
        </p>

        <div className="mt-8 flex flex-col gap-4">
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSubmit()}
            placeholder="you@company.com"
            className="rounded-xl border border-border bg-surface px-4 py-3 text-fg outline-none transition focus:border-brand"
          />
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSubmit()}
            placeholder="Password"
            className="rounded-xl border border-border bg-surface px-4 py-3 text-fg outline-none transition focus:border-brand"
          />

          {error && <p className="text-sm text-accent">{error}</p>}

          <button
            onClick={handleSubmit}
            disabled={loading}
            className="rounded-xl bg-brand px-6 py-3 font-medium text-white transition hover:opacity-90 disabled:opacity-50"
          >
            {loading ? "Please wait..." : isSignup ? "Create account" : "Sign in"}
          </button>
        </div>

        <p className="mt-6 text-center text-sm text-fg-muted">
          {isSignup ? (
            <>
              Already have an account?{" "}
              <Link href="/login" className="text-brand hover:underline">
                Sign in
              </Link>
            </>
          ) : (
            <>
              Don&apos;t have an account?{" "}
              <Link href="/signup" className="text-brand hover:underline">
                Sign up
              </Link>
            </>
          )}
        </p>
      </motion.div>
    </main>
  );
}

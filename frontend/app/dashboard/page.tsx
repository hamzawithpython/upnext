"use client";

import { motion } from "framer-motion";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import { clearToken, getCurrentUser, type CurrentUser } from "@/lib/api";

export default function DashboardPage() {
  const router = useRouter();
  const [user, setUser] = useState<CurrentUser | null>(null);

  useEffect(() => {
    getCurrentUser().then(setUser);
  }, []);

  const handleLogout = () => {
    clearToken();
    router.replace("/login");
  };

  return (
    <main className="relative min-h-screen px-6 py-12">
      <div className="glow left-1/4 top-0 h-64 w-64 bg-brand" />
      <div className="relative z-10 mx-auto max-w-4xl">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-semibold tracking-tight">Dashboard</h1>
          <button
            onClick={handleLogout}
            className="rounded-lg border border-border px-4 py-2 text-sm text-fg-muted transition hover:bg-surface hover:text-fg"
          >
            Log out
          </button>
        </div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="glass mt-8 rounded-2xl p-8"
        >
          <h2 className="text-xl font-semibold">
            Welcome{user ? `, ${user.email}` : ""} 👋
          </h2>
          <p className="mt-2 text-fg-muted">
            You&apos;re signed in. Your personalized AI intelligence feed lands
            here in Phase 4. For now, this confirms authentication and protected
            routing work end to end.
          </p>
        </motion.div>
      </div>
    </main>
  );
}

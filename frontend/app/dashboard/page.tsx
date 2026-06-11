"use client";

import { motion } from "framer-motion";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import {
  clearToken,
  getCurrentUser,
  getFeed,
  type CurrentUser,
  type FeedItem,
} from "@/lib/api";
import { FeedCard } from "@/components/feed/feed-card";
import { FeedSkeleton } from "@/components/feed/feed-skeleton";

export default function DashboardPage() {
  const router = useRouter();
  const [user, setUser] = useState<CurrentUser | null>(null);
  const [items, setItems] = useState<FeedItem[]>([]);
  const [personalized, setPersonalized] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      setUser(await getCurrentUser());
      const feed = await getFeed();
      if (feed) {
        setItems(feed.items);
        setPersonalized(feed.personalized);
      }
      setLoading(false);
    })();
  }, []);

  const handleLogout = () => {
    clearToken();
    router.replace("/login");
  };

  return (
    <main className="relative min-h-screen px-6 py-10">
      <div className="glow left-1/4 top-0 h-64 w-64 bg-brand" />
      <div className="relative z-10 mx-auto max-w-2xl">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-semibold tracking-tight">Your feed</h1>
            <p className="text-sm text-fg-muted">
              {personalized
                ? "Ranked for your interests."
                : "Top updates in AI engineering."}
            </p>
          </div>
          <div className="flex items-center gap-3">
            <button
              onClick={() => router.push("/onboarding")}
              className="rounded-lg border border-border px-4 py-2 text-sm text-fg-muted transition hover:bg-surface hover:text-fg"
            >
              Edit interests
            </button>
            <button
              onClick={handleLogout}
              className="rounded-lg border border-border px-4 py-2 text-sm text-fg-muted transition hover:bg-surface hover:text-fg"
            >
              Log out
            </button>
          </div>
        </div>

        {user && (
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="mt-6 text-sm text-fg-muted"
          >
            Signed in as {user.email}
          </motion.p>
        )}

        <div className="mt-6">
          {loading ? (
            <FeedSkeleton />
          ) : items.length === 0 ? (
            <div className="glass rounded-2xl p-8 text-center text-fg-muted">
              No feed items yet. Check back soon.
            </div>
          ) : (
            <div className="flex flex-col gap-4">
              {items.map((item, i) => (
                <FeedCard key={item.id} item={item} index={i} />
              ))}
            </div>
          )}
        </div>
      </div>
    </main>
  );
}

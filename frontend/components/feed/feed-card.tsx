"use client";

import { motion } from "framer-motion";
import { ArrowUpRight } from "lucide-react";

import type { FeedItem } from "@/lib/api";

const SOURCE_LABELS: Record<string, string> = {
  github: "GitHub",
  arxiv: "arXiv",
  reddit: "Reddit",
  hackernews: "Hacker News",
  news: "News",
  producthunt: "Product Hunt",
};

const IMPACT_STYLES: Record<string, string> = {
  high: "bg-accent/15 text-accent",
  medium: "bg-brand/15 text-brand",
  low: "bg-surface text-fg-muted",
};

function timeAgo(iso: string): string {
  const diff = Date.now() - new Date(iso).getTime();
  const hours = Math.floor(diff / 3_600_000);
  if (hours < 1) return "just now";
  if (hours < 24) return `${hours}h ago`;
  return `${Math.floor(hours / 24)}d ago`;
}

export function FeedCard({ item, index }: { item: FeedItem; index: number }) {
  return (
    <motion.a
      href={item.url}
      target="_blank"
      rel="noopener noreferrer"
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: Math.min(index * 0.05, 0.4) }}
      className="glass group block rounded-2xl p-6 transition hover:border-brand/40"
    >
      <div className="flex items-center gap-3 text-xs text-fg-muted">
        <span className="font-medium text-fg">
          {SOURCE_LABELS[item.source] ?? item.source}
        </span>
        <span>•</span>
        <span>{timeAgo(item.published_at)}</span>
        <span
          className={`ml-auto rounded-full px-2.5 py-1 font-medium ${
            IMPACT_STYLES[item.impact]
          }`}
        >
          {item.impact} impact
        </span>
      </div>

      <h3 className="mt-3 text-lg font-semibold leading-snug transition group-hover:text-brand">
        {item.title}
        <ArrowUpRight className="ml-1 inline h-4 w-4 opacity-0 transition group-hover:opacity-100" />
      </h3>

      <p className="mt-2 text-sm text-fg-muted">{item.summary}</p>

      <div className="mt-4 rounded-xl border border-border bg-surface/50 p-3">
        <span className="text-xs font-semibold uppercase tracking-wide text-brand">
          Why this matters
        </span>
        <p className="mt-1 text-sm text-fg-muted">{item.why_matters}</p>
      </div>

      <div className="mt-4 flex flex-wrap gap-2">
        {item.tags.map((tag) => (
          <span
            key={tag}
            className="rounded-full border border-border px-2.5 py-1 text-xs text-fg-muted"
          >
            {tag}
          </span>
        ))}
      </div>
    </motion.a>
  );
}

"use client";

import { motion } from "framer-motion";

export function Hero() {
  return (
    <section className="relative flex min-h-screen flex-col items-center justify-center overflow-hidden px-6 text-center">
      {/* Ambient glows */}
      <div className="glow left-1/4 top-1/4 h-72 w-72 bg-brand" />
      <div className="glow right-1/4 bottom-1/4 h-72 w-72 bg-brand-2" />
      <div className="grid-bg absolute inset-0 [mask-image:radial-gradient(ellipse_at_center,black,transparent_70%)]" />

      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, ease: "easeOut" }}
        className="relative z-10 max-w-3xl"
      >
        <div className="glass mx-auto mb-6 inline-flex items-center gap-2 rounded-full px-4 py-1.5 text-xs text-fg-muted">
          <span className="h-2 w-2 rounded-full bg-brand-2" />
          Now in private beta for AI engineers
        </div>
        <h1 className="text-5xl font-bold tracking-tight sm:text-7xl">
          The daily <span className="gradient-text">operating system</span> for AI engineers
        </h1>
        <p className="mx-auto mt-6 max-w-xl text-lg text-fg-muted">
          UpNext filters the noise from X, Reddit, GitHub, and arXiv &mdash; then ranks
          and summarizes what actually matters for your stack. Open it once a day,
          stay ahead.
        </p>
        <div className="mt-10 flex items-center justify-center gap-4">
          <a
            href="#waitlist"
            className="rounded-xl bg-brand px-6 py-3 font-medium text-white transition hover:opacity-90"
          >
            Get early access
          </a>
          <a
            href="#how"
            className="rounded-xl border border-border px-6 py-3 font-medium text-fg transition hover:bg-surface"
          >
            See how it works
          </a>
        </div>
      </motion.div>
    </section>
  );
}

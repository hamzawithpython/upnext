"use client";

import { motion } from "framer-motion";
import { useState } from "react";

export function Waitlist() {
  const [email, setEmail] = useState("");
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = () => {
    if (!email.includes("@")) return;
    // Phase 2 wires this to the backend. For now, optimistic UI.
    setSubmitted(true);
  };

  return (
    <section id="waitlist" className="relative mx-auto max-w-3xl px-6 py-32 text-center">
      <div className="glow left-1/2 top-1/2 h-64 w-64 -translate-x-1/2 -translate-y-1/2 bg-brand" />
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 0.6 }}
        className="glass relative z-10 rounded-3xl p-12"
      >
        <h2 className="text-4xl font-bold tracking-tight">
          Get ahead of <span className="gradient-text">the future</span>
        </h2>
        <p className="mx-auto mt-4 max-w-md text-fg-muted">
          Join the waitlist. We&apos;re onboarding AI engineers first.
        </p>
        {submitted ? (
          <p className="mt-8 text-brand-2">You&apos;re on the list. We&apos;ll be in touch.</p>
        ) : (
          <div className="mx-auto mt-8 flex max-w-md gap-3">
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@company.com"
              className="flex-1 rounded-xl border border-border bg-surface px-4 py-3 text-fg outline-none transition focus:border-brand"
            />
            <button
              onClick={handleSubmit}
              className="rounded-xl bg-brand px-6 py-3 font-medium text-white transition hover:opacity-90"
            >
              Join
            </button>
          </div>
        )}
      </motion.div>
    </section>
  );
}

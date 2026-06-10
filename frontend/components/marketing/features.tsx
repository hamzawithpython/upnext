"use client";

import { motion } from "framer-motion";
import { Filter, Sparkles, Target, Zap } from "lucide-react";

const features = [
  { icon: Filter, title: "Signal over noise", desc: "We strip the hype and surface only what moves your field forward." },
  { icon: Sparkles, title: "AI summaries", desc: "Every item comes with a concise summary and a clear 'why this matters'." },
  { icon: Target, title: "Personalized feed", desc: "Tuned to your stack — RAG, agents, MCP, automation, whatever you build." },
  { icon: Zap, title: "Daily digest", desc: "One structured intelligence brief, delivered on your schedule." },
];

export function Features() {
  return (
    <section id="features" className="relative mx-auto max-w-5xl px-6 py-32">
      <h2 className="text-center text-4xl font-bold tracking-tight sm:text-5xl">
        Built for people who <span className="gradient-text">ship</span>
      </h2>
      <div className="mt-16 grid gap-6 sm:grid-cols-2">
        {features.map((f, i) => (
          <motion.div
            key={f.title}
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-80px" }}
            transition={{ duration: 0.5, delay: i * 0.1 }}
            className="glass rounded-2xl p-8 transition hover:border-brand/40"
          >
            <f.icon className="h-8 w-8 text-brand" />
            <h3 className="mt-4 text-xl font-semibold">{f.title}</h3>
            <p className="mt-2 text-fg-muted">{f.desc}</p>
          </motion.div>
        ))}
      </div>
    </section>
  );
}

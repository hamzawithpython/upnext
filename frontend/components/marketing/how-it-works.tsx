"use client";

import { motion } from "framer-motion";

const steps = [
  { n: "01", title: "We collect", desc: "Pull from GitHub, arXiv, Reddit, Hacker News, and curated sources continuously." },
  { n: "02", title: "We rank", desc: "Score every item by relevance to your interests and real-world impact." },
  { n: "03", title: "We summarize", desc: "Generate a tight summary and impact tag so you decide in seconds." },
];

export function HowItWorks() {
  return (
    <section id="how" className="relative mx-auto max-w-5xl px-6 py-32">
      <h2 className="text-center text-4xl font-bold tracking-tight sm:text-5xl">
        How <span className="gradient-text">UpNext</span> works
      </h2>
      <div className="mt-16 grid gap-8 md:grid-cols-3">
        {steps.map((s, i) => (
          <motion.div
            key={s.n}
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-80px" }}
            transition={{ duration: 0.5, delay: i * 0.15 }}
            className="relative"
          >
            <span className="gradient-text text-5xl font-bold">{s.n}</span>
            <h3 className="mt-4 text-xl font-semibold">{s.title}</h3>
            <p className="mt-2 text-fg-muted">{s.desc}</p>
          </motion.div>
        ))}
      </div>
    </section>
  );
}

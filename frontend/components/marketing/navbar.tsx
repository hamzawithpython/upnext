"use client";

import { motion } from "framer-motion";
import { Zap } from "lucide-react";

export function Navbar() {
  return (
    <motion.nav
      initial={{ y: -20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.6, ease: "easeOut" }}
      className="fixed top-0 z-50 w-full"
    >
      <div className="glass mx-auto mt-4 flex max-w-5xl items-center justify-between rounded-2xl px-6 py-3">
        <div className="flex items-center gap-2">
          <Zap className="h-5 w-5 text-brand" />
          <span className="text-lg font-semibold tracking-tight">UpNext</span>
        </div>
        <div className="hidden items-center gap-8 text-sm text-fg-muted md:flex">
          <a href="#features" className="transition hover:text-fg">Features</a>
          <a href="#how" className="transition hover:text-fg">How it works</a>
          <a href="#waitlist" className="transition hover:text-fg">Waitlist</a>
        </div>
        <a
          href="#waitlist"
          className="rounded-lg bg-brand px-4 py-2 text-sm font-medium text-white transition hover:opacity-90"
        >
          Join waitlist
        </a>
      </div>
    </motion.nav>
  );
}

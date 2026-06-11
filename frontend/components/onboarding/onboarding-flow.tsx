"use client";

import { AnimatePresence, motion } from "framer-motion";
import { useRouter } from "next/navigation";
import { useState } from "react";

import {
  CONTENT_STYLES,
  GOALS,
  INTERESTS,
  SKILL_LEVELS,
  TOOLS,
} from "@/lib/onboarding-options";
import { savePreferences, type Preferences } from "@/lib/api";

function toggle(list: string[], value: string): string[] {
  return list.includes(value)
    ? list.filter((v) => v !== value)
    : [...list, value];
}

function Chip({
  label,
  selected,
  onClick,
}: {
  label: string;
  selected: boolean;
  onClick: () => void;
}) {
  return (
    <button
      onClick={onClick}
      className={`rounded-full border px-4 py-2 text-sm transition ${
        selected
          ? "border-brand bg-brand/15 text-fg"
          : "border-border bg-surface text-fg-muted hover:border-brand/40 hover:text-fg"
      }`}
    >
      {label}
    </button>
  );
}

export function OnboardingFlow({ existing }: { existing?: Preferences | null }) {
  const router = useRouter();
  const [step, setStep] = useState(0);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [skillLevel, setSkillLevel] = useState<string | null>(
    existing?.skill_level ?? null
  );
  const [interests, setInterests] = useState<string[]>(existing?.interests ?? []);
  const [tools, setTools] = useState<string[]>(existing?.tools ?? []);
  const [goals, setGoals] = useState<string[]>(existing?.goals ?? []);
  const [contentStyle, setContentStyle] = useState<string | null>(
    existing?.content_style ?? null
  );

  const steps = [
    {
      title: "What's your experience level?",
      subtitle: "We tune depth and difficulty to match.",
      canProceed: skillLevel !== null,
      content: (
        <div className="flex flex-col gap-3">
          {SKILL_LEVELS.map((s) => (
            <button
              key={s.value}
              onClick={() => setSkillLevel(s.value)}
              className={`rounded-xl border p-4 text-left transition ${
                skillLevel === s.value
                  ? "border-brand bg-brand/15"
                  : "border-border bg-surface hover:border-brand/40"
              }`}
            >
              <div className="font-medium">{s.label}</div>
              <div className="text-sm text-fg-muted">{s.desc}</div>
            </button>
          ))}
        </div>
      ),
    },
    {
      title: "What are you into?",
      subtitle: "Pick the topics you want in your feed.",
      canProceed: interests.length > 0,
      content: (
        <div className="flex flex-wrap gap-2">
          {INTERESTS.map((i) => (
            <Chip
              key={i}
              label={i}
              selected={interests.includes(i)}
              onClick={() => setInterests(toggle(interests, i))}
            />
          ))}
        </div>
      ),
    },
    {
      title: "Which tools do you use?",
      subtitle: "We prioritize updates relevant to your stack.",
      canProceed: tools.length > 0,
      content: (
        <div className="flex flex-wrap gap-2">
          {TOOLS.map((t) => (
            <Chip
              key={t}
              label={t}
              selected={tools.includes(t)}
              onClick={() => setTools(toggle(tools, t))}
            />
          ))}
        </div>
      ),
    },
    {
      title: "What are your goals?",
      subtitle: "This shapes what we surface and why.",
      canProceed: goals.length > 0,
      content: (
        <div className="flex flex-wrap gap-2">
          {GOALS.map((g) => (
            <Chip
              key={g}
              label={g}
              selected={goals.includes(g)}
              onClick={() => setGoals(toggle(goals, g))}
            />
          ))}
        </div>
      ),
    },
    {
      title: "How do you like your updates?",
      subtitle: "You can change this anytime.",
      canProceed: contentStyle !== null,
      content: (
        <div className="flex flex-col gap-3">
          {CONTENT_STYLES.map((c) => (
            <button
              key={c.value}
              onClick={() => setContentStyle(c.value)}
              className={`rounded-xl border p-4 text-left transition ${
                contentStyle === c.value
                  ? "border-brand bg-brand/15"
                  : "border-border bg-surface hover:border-brand/40"
              }`}
            >
              <div className="font-medium">{c.label}</div>
              <div className="text-sm text-fg-muted">{c.desc}</div>
            </button>
          ))}
        </div>
      ),
    },
  ];

  const current = steps[step];
  const isLast = step === steps.length - 1;

  const handleNext = async () => {
    setError(null);
    if (!isLast) {
      setStep((s) => s + 1);
      return;
    }
    setSaving(true);
    try {
      await savePreferences({
        skill_level: skillLevel,
        interests,
        tools,
        goals,
        content_style: contentStyle,
      });
      router.push("/dashboard");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong.");
    } finally {
      setSaving(false);
    }
  };

  return (
    <main className="relative flex min-h-screen items-center justify-center px-6">
      <div className="glow left-1/2 top-1/4 h-72 w-72 -translate-x-1/2 bg-brand" />
      <div className="relative z-10 w-full max-w-lg">
        {/* Progress */}
        <div className="mb-8 flex gap-2">
          {steps.map((_, i) => (
            <div
              key={i}
              className={`h-1 flex-1 rounded-full transition ${
                i <= step ? "bg-brand" : "bg-border"
              }`}
            />
          ))}
        </div>

        <AnimatePresence mode="wait">
          <motion.div
            key={step}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            transition={{ duration: 0.3 }}
            className="glass rounded-3xl p-8"
          >
            <h1 className="text-2xl font-bold tracking-tight">{current.title}</h1>
            <p className="mt-2 text-sm text-fg-muted">{current.subtitle}</p>
            <div className="mt-6">{current.content}</div>

            {error && <p className="mt-4 text-sm text-accent">{error}</p>}

            <div className="mt-8 flex items-center justify-between">
              <button
                onClick={() => setStep((s) => Math.max(0, s - 1))}
                disabled={step === 0}
                className="text-sm text-fg-muted transition hover:text-fg disabled:opacity-0"
              >
                Back
              </button>
              <button
                onClick={handleNext}
                disabled={!current.canProceed || saving}
                className="rounded-xl bg-brand px-6 py-3 font-medium text-white transition hover:opacity-90 disabled:opacity-40"
              >
                {saving ? "Saving..." : isLast ? "Finish" : "Continue"}
              </button>
            </div>
          </motion.div>
        </AnimatePresence>
      </div>
    </main>
  );
}

"use client";

import { AnimatePresence, motion } from "framer-motion";
import { Send, Sparkles, X } from "lucide-react";
import { useEffect, useRef, useState } from "react";

import { streamAssistant, type ChatMessage } from "@/lib/api";

const SUGGESTIONS = [
  "What should I learn next?",
  "Explain MCP in simple terms",
  "Summarize today's top item",
];

export function AssistantPanel() {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [streaming, setStreaming] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight });
  }, [messages]);

  const send = async (text: string) => {
    const content = text.trim();
    if (!content || streaming) return;

    const userMsg: ChatMessage = { role: "user", content };
    const history = [...messages, userMsg];
    setMessages([...history, { role: "assistant", content: "" }]);
    setInput("");
    setStreaming(true);

    try {
      await streamAssistant(history, (chunk) => {
        setMessages((prev) => {
          const next = [...prev];
          next[next.length - 1] = {
            role: "assistant",
            content: next[next.length - 1].content + chunk,
          };
          return next;
        });
      });
    } catch {
      setMessages((prev) => {
        const next = [...prev];
        next[next.length - 1] = {
          role: "assistant",
          content: "Sorry, I couldn't respond right now. Please try again.",
        };
        return next;
      });
    } finally {
      setStreaming(false);
    }
  };

  return (
    <>
      {/* Floating launcher */}
      <button
        onClick={() => setOpen(true)}
        className="fixed bottom-6 right-6 z-40 flex items-center gap-2 rounded-full bg-brand px-5 py-3 font-medium text-white shadow-lg transition hover:opacity-90"
      >
        <Sparkles className="h-4 w-4" />
        Ask UpNext
      </button>

      <AnimatePresence>
        {open && (
          <>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setOpen(false)}
              className="fixed inset-0 z-40 bg-black/40 backdrop-blur-sm"
            />
            <motion.aside
              initial={{ x: "100%" }}
              animate={{ x: 0 }}
              exit={{ x: "100%" }}
              transition={{ type: "spring", damping: 28, stiffness: 260 }}
              className="fixed right-0 top-0 z-50 flex h-full w-full max-w-md flex-col border-l border-border bg-bg-soft"
            >
              <div className="flex items-center justify-between border-b border-border px-6 py-4">
                <div className="flex items-center gap-2">
                  <Sparkles className="h-5 w-5 text-brand" />
                  <span className="font-semibold">UpNext Assistant</span>
                </div>
                <button
                  onClick={() => setOpen(false)}
                  className="text-fg-muted transition hover:text-fg"
                >
                  <X className="h-5 w-5" />
                </button>
              </div>

              <div ref={scrollRef} className="flex-1 overflow-y-auto px-6 py-4">
                {messages.length === 0 ? (
                  <div className="mt-8 text-center">
                    <p className="text-sm text-fg-muted">
                      Ask anything about AI engineering, your feed, or what to
                      learn next.
                    </p>
                    <div className="mt-6 flex flex-col gap-2">
                      {SUGGESTIONS.map((s) => (
                        <button
                          key={s}
                          onClick={() => send(s)}
                          className="rounded-xl border border-border bg-surface px-4 py-2.5 text-left text-sm text-fg-muted transition hover:border-brand/40 hover:text-fg"
                        >
                          {s}
                        </button>
                      ))}
                    </div>
                  </div>
                ) : (
                  <div className="flex flex-col gap-4">
                    {messages.map((m, i) => (
                      <div
                        key={i}
                        className={`max-w-[85%] rounded-2xl px-4 py-3 text-sm ${
                          m.role === "user"
                            ? "ml-auto bg-brand text-white"
                            : "bg-surface text-fg"
                        }`}
                      >
                        {m.content || (
                          <span className="inline-flex gap-1">
                            <span className="h-2 w-2 animate-pulse rounded-full bg-fg-muted" />
                            <span className="h-2 w-2 animate-pulse rounded-full bg-fg-muted [animation-delay:150ms]" />
                            <span className="h-2 w-2 animate-pulse rounded-full bg-fg-muted [animation-delay:300ms]" />
                          </span>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </div>

              <div className="border-t border-border p-4">
                <div className="flex gap-2">
                  <input
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && send(input)}
                    placeholder="Ask anything..."
                    disabled={streaming}
                    className="flex-1 rounded-xl border border-border bg-surface px-4 py-3 text-sm text-fg outline-none transition focus:border-brand disabled:opacity-50"
                  />
                  <button
                    onClick={() => send(input)}
                    disabled={streaming || !input.trim()}
                    className="rounded-xl bg-brand px-4 text-white transition hover:opacity-90 disabled:opacity-40"
                  >
                    <Send className="h-4 w-4" />
                  </button>
                </div>
              </div>
            </motion.aside>
          </>
        )}
      </AnimatePresence>
    </>
  );
}

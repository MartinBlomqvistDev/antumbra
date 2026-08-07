"use client";

import { useState } from "react";
import { AnswerList, type Answer } from "@/components/answers";
import type { Copy } from "@/content/types";

/**
 * The live search box. Rendered only when the site was built with
 * NEXT_PUBLIC_ANTUMBRA_API set; the page works in full without it, on the
 * baked examples. Queries go to the API and nowhere else.
 */
export function Search({
  apiBase,
  labels,
  locale,
}: {
  apiBase: string;
  labels: Copy["uppslag"];
  locale: string;
}) {
  const [question, setQuestion] = useState("");
  const [answers, setAnswers] = useState<Answer[] | null>(null);
  const [state, setState] = useState<"idle" | "searching" | "error">("idle");

  async function submit(event: React.FormEvent) {
    event.preventDefault();
    if (!question.trim()) return;
    setState("searching");
    try {
      const response = await fetch(
        `${apiBase}/ask?q=${encodeURIComponent(question.trim())}`,
      );
      if (!response.ok) throw new Error(String(response.status));
      const payload = (await response.json()) as { answers: Answer[] };
      setAnswers(payload.answers);
      setState("idle");
    } catch {
      setState("error");
    }
  }

  return (
    <div className="max-w-2xl space-y-4">
      <form onSubmit={submit} className="flex gap-2">
        <label htmlFor="corpus-search" className="sr-only">
          {labels.search.label}
        </label>
        <input
          id="corpus-search"
          type="search"
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          maxLength={500}
          className="w-full rounded-md border border-border-soft bg-surface px-3 py-2 text-sm"
        />
        <button
          type="submit"
          disabled={state === "searching"}
          className="rounded-md bg-accent px-4 py-2 text-sm font-semibold text-white disabled:opacity-60"
        >
          {state === "searching"
            ? labels.search.searching
            : labels.search.button}
        </button>
      </form>
      {state === "error" ? (
        <p className="text-sm text-ink-secondary">{labels.search.error}</p>
      ) : null}
      {answers !== null && state === "idle" ? (
        <AnswerList answers={answers} labels={labels} locale={locale} />
      ) : null}
    </div>
  );
}

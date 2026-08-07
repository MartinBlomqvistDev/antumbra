import type { Copy } from "@/content/types";

/** One answer from the quotation apparatus, baked or live. */
export type Answer = {
  text: string;
  ref: string;
  country: string;
  number: number;
  score: number;
};

/**
 * Renders answers the only way the site ever shows them: the verbatim
 * quotation, then country, reference, paragraph number and similarity.
 * Works identically for baked examples and live results.
 */
export function AnswerList({
  answers,
  labels,
  locale,
}: {
  answers: Answer[];
  labels: Pick<Copy["uppslag"], "similarity" | "noAnswers">;
  locale: string;
}) {
  if (answers.length === 0) {
    return <p className="text-sm text-ink-secondary">{labels.noAnswers}</p>;
  }
  const decimal = new Intl.NumberFormat(locale, {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });
  return (
    <div className="space-y-4">
      {answers.map((answer) => (
        <blockquote
          key={`${answer.ref}-${answer.number}-${answer.score}`}
          className="border-l-2 border-accent pl-3"
        >
          <p className="text-sm">{answer.text}</p>
          <footer className="mt-1 text-xs text-ink-secondary">
            {answer.country} · {answer.ref} §{answer.number} ·{" "}
            {labels.similarity} {decimal.format(answer.score)}
          </footer>
        </blockquote>
      ))}
    </div>
  );
}

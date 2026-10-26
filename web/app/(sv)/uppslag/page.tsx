import type { Metadata } from "next";
import { AnswerList } from "@/components/answers";
import { PageIntro } from "@/components/shell";
import { sv } from "@/content/sv";
import { readExamples } from "@/lib/data";

export const metadata: Metadata = { title: sv.uppslag.title };

/**
 * The six baked answers, and why the search box above them is gone.
 *
 * Retrieval was measured on 26 October 2026 against questions built from the
 * citation graph. The hybrid that answered here came third of three, behind
 * plain BM25 on every figure, and the condition written before the measurement
 * said such a box goes. The examples stay: they run through the same code and
 * every quotation can be checked against its source paragraph.
 */
export default function Uppslag() {
  const examples = readExamples();
  return (
    <div className="space-y-8">
      <PageIntro title={sv.uppslag.title} lead={sv.uppslag.lead} />
      <p className="max-w-2xl border border-border-soft p-4 text-sm">
        {sv.uppslag.banner}
      </p>
      <section className="max-w-2xl space-y-3">
        <h2 className="text-2xl font-semibold tracking-tight">
          {sv.uppslag.matning.heading}
        </h2>
        {sv.uppslag.matning.body.map((paragraph) => (
          <p key={paragraph.slice(0, 40)} className="text-sm text-ink-secondary">
            {paragraph}
          </p>
        ))}
      </section>
      <section className="max-w-2xl space-y-3">
        <h2 className="text-2xl font-semibold tracking-tight">
          {sv.uppslag.examplesHeading}
        </h2>
        {examples.map((example, index) => (
          <details
            key={example.question}
            open={index === 0}
            className="border border-border-soft"
          >
            <summary className="cursor-pointer p-4 text-sm font-semibold">
              {example.question}
            </summary>
            <div className="border-t border-border-soft p-4">
              <AnswerList
                answers={example.answers}
                labels={sv.uppslag}
                locale="sv-SE"
              />
            </div>
          </details>
        ))}
      </section>
    </div>
  );
}

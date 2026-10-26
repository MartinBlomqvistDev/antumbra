import type { Metadata } from "next";
import { AnswerList } from "@/components/answers";
import { Search } from "@/components/search";
import { PageIntro } from "@/components/shell";
import { sv } from "@/content/sv";
import { readExamples } from "@/lib/data";

export const metadata: Metadata = { title: sv.uppslag.title };

const apiBase = process.env.NEXT_PUBLIC_ANTUMBRA_API;

export default function Uppslag() {
  const examples = readExamples();
  return (
    <div className="space-y-8">
      <PageIntro title={sv.uppslag.title} lead={sv.uppslag.lead} />
      <p className="max-w-2xl border border-border-soft p-4 text-sm">
        {sv.uppslag.banner}
      </p>
      {apiBase ? (
        <Search apiBase={apiBase} labels={sv.uppslag} locale="sv-SE" />
      ) : (
        <p className="max-w-2xl text-sm text-ink-secondary">
          {sv.uppslag.search.note}
        </p>
      )}
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

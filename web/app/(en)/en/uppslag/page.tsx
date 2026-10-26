import type { Metadata } from "next";
import { AnswerList } from "@/components/answers";
import { Search } from "@/components/search";
import { PageIntro } from "@/components/shell";
import { en } from "@/content/en";
import { readExamples } from "@/lib/data";

export const metadata: Metadata = { title: en.uppslag.title };

const apiBase = process.env.NEXT_PUBLIC_ANTUMBRA_API;

export default function Reference() {
  const examples = readExamples();
  return (
    <div className="space-y-8">
      <PageIntro title={en.uppslag.title} lead={en.uppslag.lead} />
      <p className="max-w-2xl border border-border-soft p-4 text-sm">
        {en.uppslag.banner}
      </p>
      {apiBase ? (
        <Search apiBase={apiBase} labels={en.uppslag} locale="en-GB" />
      ) : (
        <p className="max-w-2xl text-sm text-ink-secondary">
          {en.uppslag.search.note}
        </p>
      )}
      <section className="max-w-2xl space-y-3">
        <h2 className="text-2xl font-semibold tracking-tight">
          {en.uppslag.examplesHeading}
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
                labels={en.uppslag}
                locale="en-GB"
              />
            </div>
          </details>
        ))}
      </section>
    </div>
  );
}

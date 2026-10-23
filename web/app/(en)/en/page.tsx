import Link from "next/link";
import { ChainExample } from "@/components/chain-example";
import { en } from "@/content/en";
import { readHeadline } from "@/lib/data";
import { readSweden } from "@/lib/sverige";

export default function Home() {
  const headline = readHeadline();
  const sverige = readSweden();
  const count = new Intl.NumberFormat("en-GB");
  const percent = new Intl.NumberFormat("en-GB", {
    style: "percent",
    maximumFractionDigits: 1,
  });
  // Same order as the Swedish page: the finding first, read from the export.
  const classLabel = (template: string, klass: "A" | "B") =>
    template
      .replace("{dokument}", count.format(sverige.klasser[klass].dokument))
      .replace("{lan}", count.format(sverige.klasser[klass].myndigheter));
  const sweden = [
    {
      value: percent.format(sverige.klasser.A.andel),
      label: classLabel(en.home.swedenLabels!.classA, "A"),
    },
    {
      value: percent.format(sverige.klasser.B.andel),
      label: classLabel(en.home.swedenLabels!.classB, "B"),
    },
    {
      value: en.home.swedenLabels!.paidValue,
      label: en.home.swedenLabels!.paid,
    },
  ];
  const eu = [
    { value: count.format(headline.audits), label: en.home.numberLabels.audits },
    {
      value: count.format(headline.recommendations),
      label: en.home.numberLabels.recommendations,
    },
    {
      value: percent.format(headline.share_citations_resolved),
      label: en.home.numberLabels.citationsResolved,
    },
  ];
  return (
    <div className="space-y-12 py-6">
      <div className="max-w-3xl space-y-5">
        <p className="text-xs font-semibold uppercase tracking-widest text-accent">
          {en.home.kicker}
        </p>
        <h1 className="font-display text-5xl font-semibold leading-tight tracking-tight sm:text-6xl">
          {en.site.tagline}
        </h1>
        <p className="max-w-2xl text-lg text-ink-secondary">{en.home.lead}</p>
      </div>
      <section className="space-y-3">
        <h2 className="text-sm font-semibold uppercase tracking-wide text-ink-secondary">
          <Link href="/en/sverige/" className="hover:text-ink">
            {en.home.swedenHeading}
          </Link>
        </h2>
        <dl className="grid gap-6 sm:grid-cols-3">
          {sweden.map((item) => (
            <div
              key={item.label}
              className="border-t-2 border-accent bg-surface-raised p-5"
            >
              <dd className="font-display text-4xl font-semibold tabular-nums">
                {item.value}
              </dd>
              <dt className="mt-2 text-sm text-ink-secondary">{item.label}</dt>
            </div>
          ))}
        </dl>
      </section>
      <section className="space-y-3">
        <h2 className="text-sm font-semibold uppercase tracking-wide text-ink-secondary">
          <Link href="/en/jamforelse/" className="hover:text-ink">
            {en.home.euHeading}
          </Link>
        </h2>
        <dl className="grid gap-6 sm:grid-cols-3">
          {eu.map((item) => (
            <div
              key={item.label}
              className="border-t-2 border-accent-warm bg-surface-raised p-5"
            >
              <dd className="font-display text-4xl font-semibold tabular-nums">
                {item.value}
              </dd>
              <dt className="mt-2 text-sm text-ink-secondary">{item.label}</dt>
            </div>
          ))}
        </dl>
      </section>
      <ChainExample copy={en} locale="en-GB" hrefBase="/en/jamforelse/" />
    </div>
  );
}

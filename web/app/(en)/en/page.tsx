import { en } from "@/content/en";
import { readHeadline } from "@/lib/data";

export default function Home() {
  const headline = readHeadline();
  const count = new Intl.NumberFormat("en-GB");
  const percent = new Intl.NumberFormat("en-GB", {
    style: "percent",
    maximumFractionDigits: 1,
  });
  const numbers = [
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
    <div className="space-y-14 py-6">
      <div className="max-w-3xl space-y-5">
        <p className="text-xs font-semibold uppercase tracking-widest text-accent">
          {en.home.kicker}
        </p>
        <h1 className="font-display text-5xl font-semibold leading-tight tracking-tight sm:text-6xl">
          {en.site.tagline}
        </h1>
        <p className="max-w-2xl text-lg text-ink-secondary">{en.home.lead}</p>
      </div>
      <dl className="grid gap-6 sm:grid-cols-3">
        {numbers.map((item) => (
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
    </div>
  );
}

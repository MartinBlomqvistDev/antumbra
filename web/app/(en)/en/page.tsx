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
    <div className="space-y-10">
      <div className="max-w-2xl space-y-4">
        <h1 className="text-3xl font-semibold tracking-tight">
          {en.site.tagline}
        </h1>
        <p className="text-lg text-ink-secondary">{en.home.lead}</p>
      </div>
      <dl className="grid gap-6 sm:grid-cols-3">
        {numbers.map((item) => (
          <div
            key={item.label}
            className="rounded-lg border border-border-soft bg-surface-raised p-5"
          >
            <dt className="text-sm text-ink-secondary">{item.label}</dt>
            <dd className="mt-1 text-3xl font-semibold tabular-nums">
              {item.value}
            </dd>
          </div>
        ))}
      </dl>
    </div>
  );
}

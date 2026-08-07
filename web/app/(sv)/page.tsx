import Link from "next/link";
import { ChainExample } from "@/components/chain-example";
import { sv } from "@/content/sv";
import { readHeadline } from "@/lib/data";
import { swedenStats } from "@/lib/stats";

export default function Home() {
  const headline = readHeadline();
  const stats = swedenStats();
  const count = new Intl.NumberFormat("sv-SE");
  const percent = new Intl.NumberFormat("sv-SE", {
    style: "percent",
    maximumFractionDigits: 1,
  });
  const sweden = [
    { value: count.format(stats.sent), label: sv.home.swedenLabels!.sent },
    { value: count.format(stats.files), label: sv.home.swedenLabels!.files },
    {
      value: sv.home.swedenLabels!.paidValue,
      label: sv.home.swedenLabels!.paid,
    },
  ];
  const eu = [
    { value: count.format(headline.audits), label: sv.home.numberLabels.audits },
    {
      value: count.format(headline.recommendations),
      label: sv.home.numberLabels.recommendations,
    },
    {
      value: percent.format(headline.share_citations_resolved),
      label: sv.home.numberLabels.citationsResolved,
    },
  ];
  return (
    <div className="space-y-12 py-6">
      <div className="max-w-3xl space-y-5">
        <p className="text-xs font-semibold uppercase tracking-widest text-accent">
          {sv.home.kicker}
        </p>
        <h1 className="font-display text-5xl font-semibold leading-tight tracking-tight sm:text-6xl">
          {sv.site.tagline}
        </h1>
        <p className="max-w-2xl text-lg text-ink-secondary">{sv.home.lead}</p>
      </div>
      <section className="space-y-3">
        <h2 className="text-sm font-semibold uppercase tracking-wide text-ink-secondary">
          <Link href="/sverige/" className="hover:text-ink">
            {sv.home.swedenHeading}
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
          <Link href="/jamforelse/" className="hover:text-ink">
            {sv.home.euHeading}
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
      <ChainExample copy={sv} locale="sv-SE" hrefBase="/jamforelse/" />
    </div>
  );
}

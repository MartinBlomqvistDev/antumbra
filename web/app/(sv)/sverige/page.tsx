import type { Metadata } from "next";
import Link from "next/link";
import { PageIntro } from "@/components/shell";
import { sv } from "@/content/sv";
import { swedenStats } from "@/lib/stats";

const copy = sv.sverige!;

export const metadata: Metadata = { title: copy.title };

export default function Sverige() {
  const stats = swedenStats();
  const count = new Intl.NumberFormat("sv-SE");
  const overview = [
    { value: count.format(stats.sent), label: copy.overview.sent },
    { value: count.format(stats.files), label: copy.overview.files },
    {
      value: count.format(stats.deliveringAuthorities),
      label: copy.overview.deliveringAuthorities,
    },
    {
      value: count.format(stats.feeNotices),
      label: copy.overview.feeNotices,
    },
    {
      value: count.format(stats.feeStopped.length),
      label: copy.overview.feeStopped,
    },
    { value: copy.overview.paidValue, label: copy.overview.paid },
  ];
  return (
    <div className="space-y-12">
      <PageIntro title={copy.title} lead={copy.lead} />
      <section className="max-w-2xl space-y-2">
        <h2 className="font-display text-2xl font-semibold tracking-tight">
          {copy.design.heading}
        </h2>
        <p className="text-sm text-ink-secondary">{copy.design.body}</p>
        <p className="text-sm text-ink-secondary">{copy.processNote}</p>
      </section>
      <section className="space-y-3">
        <h2 className="font-display text-2xl font-semibold tracking-tight">
          {copy.overview.heading}
        </h2>
        <dl className="grid gap-6 sm:grid-cols-3">
          {overview.map((item) => (
            <div
              key={item.label}
              className="border-t-2 border-accent bg-surface-raised p-5"
            >
              <dd className="font-display text-3xl font-semibold tabular-nums">
                {item.value}
              </dd>
              <dt className="mt-2 text-sm text-ink-secondary">{item.label}</dt>
            </div>
          ))}
        </dl>
        <p className="text-sm text-ink-secondary">
          <Link
            href="/handlingar/"
            className="text-accent underline underline-offset-2"
          >
            {copy.toHandlingar}
          </Link>
        </p>
      </section>
      <section className="max-w-2xl space-y-3">
        <h2 className="font-display text-2xl font-semibold tracking-tight">
          {copy.wordings.heading}
        </h2>
        <p className="text-sm text-ink-secondary">{copy.wordings.note}</p>
        <div className="space-y-2">
          {copy.wordings.items.map((item) => (
            <details
              key={item.label}
              className="rounded-lg border border-border-soft bg-surface-raised"
            >
              <summary className="cursor-pointer p-3 text-sm font-semibold">
                {item.label}
              </summary>
              <p className="whitespace-pre-line border-t border-border-soft p-4 text-sm">
                {item.text}
              </p>
            </details>
          ))}
        </div>
      </section>
      <section className="max-w-2xl space-y-3">
        <h2 className="font-display text-2xl font-semibold tracking-tight">
          {copy.feeStopped.heading}
        </h2>
        <p className="text-sm text-ink-secondary">{copy.feeStopped.note}</p>
        <ul className="space-y-1 text-sm">
          {stats.feeStopped.map((entry) => (
            <li key={entry}>{entry}</li>
          ))}
        </ul>
      </section>
    </div>
  );
}

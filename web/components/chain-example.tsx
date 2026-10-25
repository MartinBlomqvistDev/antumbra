import Link from "next/link";
import type { Copy } from "@/content/types";
import {
  countryTotals,
  readCountryYears,
  readUnderlag,
} from "@/lib/underlag";

/**
 * The signature interaction, shown as four visible steps built from the
 * real Swedish underlag: aggregate, rows, verbatim paragraph, document
 * with checksum. Everything is chosen at build time from the newest audit
 * whose chain resolves, so the example is always live data, never a
 * mock-up.
 */
export function ChainExample({
  copy,
  locale,
  hrefBase,
}: {
  copy: Copy;
  locale: string;
  hrefBase: string;
}) {
  const count = new Intl.NumberFormat(locale);
  const totals = countryTotals(readCountryYears()).find(
    (row) => row.slug === "sweden",
  )!;
  const underlag = readUnderlag("sweden");
  const audits = [...underlag.audits].sort(
    (a, b) => (b.year ?? 0) - (a.year ?? 0) || a.ref.localeCompare(b.ref),
  );
  const audit = audits.find((candidate) =>
    candidate.recommendations.some((rec) =>
      rec.citations.some((citation) => citation.resolved),
    ),
  )!;
  const recommendation = audit.recommendations.find((rec) =>
    rec.citations.some((citation) => citation.resolved),
  )!;
  const citation = recommendation.citations.find(
    (candidate) => candidate.resolved,
  )!;
  const labels = copy.home.chain;
  const steps = [
    {
      label: labels.steps.figure,
      body: (
        <p>
          <span className="text-3xl font-semibold tabular-nums">
            {count.format(totals.recommendations)}
          </span>{" "}
          <span className="text-ink-secondary">{labels.figureLead}</span>
        </p>
      ),
    },
    {
      label: labels.steps.rows,
      body: (
        <p className="text-sm">
          {audit.ref}
          {audit.year !== null ? (
            <span className="text-ink-secondary"> · {audit.year}</span>
          ) : null}
          {audit.title ? (
            <span className="text-ink-secondary"> · {audit.title}</span>
          ) : null}
          <br />
          <span className="font-semibold">
            {copy.chain.recommendationLabel} {recommendation.number}.
          </span>{" "}
          {recommendation.text.length > 180
            ? `${recommendation.text.slice(0, 180)}…`
            : recommendation.text}
        </p>
      ),
    },
    {
      label: labels.steps.paragraph,
      body: (
        <blockquote className="border-l-2 border-ink pl-3 text-sm">
          <p>{citation.text}</p>
          <footer className="mt-1 text-xs text-ink-secondary">
            {citation.cites}
            {citation.number !== null ? ` §${citation.number}` : null}
          </footer>
        </blockquote>
      ),
    },
    {
      label: labels.steps.document,
      body: (
        <p className="text-xs text-ink-secondary">
          <span className="break-all">{audit.report_path}</span>
          {audit.sha256 ? (
            <>
              {" · "}
              {copy.chain.checksum}{" "}
              <code className="break-all">{audit.sha256}</code>
            </>
          ) : null}
        </p>
      ),
    },
  ];
  return (
    <section className="space-y-4">
      <h2 className="text-2xl font-semibold tracking-tight">
        {labels.heading}
      </h2>
      <p className="max-w-2xl text-sm text-ink-secondary">{labels.intro}</p>
      <ol className="max-w-2xl space-y-0">
        {steps.map((step, index) => (
          <li
            key={step.label}
            className={`border-l-2 border-ink pl-4 ${
              index < steps.length - 1 ? "pb-5" : ""
            }`}
          >
            <p className="fieldname">
              {index + 1} · {step.label}
            </p>
            <div className="mt-1">{step.body}</div>
          </li>
        ))}
      </ol>
      <p className="text-sm">
        <Link
          href={`${hrefBase}sweden/`}
          className="text-ink underline underline-offset-2"
        >
          {labels.toCountry}
        </Link>
      </p>
    </section>
  );
}

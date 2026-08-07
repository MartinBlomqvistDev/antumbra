import { ChartSection, ColumnChart, ShareBars } from "@/components/charts";
import { CountryTable } from "@/components/country-table";
import { PageIntro } from "@/components/shell";
import type { Copy } from "@/content/types";
import {
  byYear,
  chainClosureByCountry,
  countryTotals,
  readCountryYears,
} from "@/lib/underlag";

/** The whole comparison view, shared by the two language routes. */
export function JamforelseView({
  copy,
  locale,
  hrefBase,
}: {
  copy: Copy;
  locale: string;
  hrefBase: string;
}) {
  const rows = readCountryYears();
  const totals = countryTotals(rows);
  const years = byYear(rows);
  const chain = chainClosureByCountry();
  const count = new Intl.NumberFormat(locale);
  const percent = new Intl.NumberFormat(locale, {
    style: "percent",
    maximumFractionDigits: 0,
  });
  const labels = copy.jamforelse.charts;
  const shareTable = (
    input: { label: string; numerator: number; total: number }[],
  ) => ({
    headers: [
      copy.jamforelse.table.country,
      copy.jamforelse.table.recommendations,
      labels.shareHeader,
    ],
    rows: input
      .sort((a, b) => b.numerator / b.total - a.numerator / a.total)
      .map((row) => [
        row.label,
        `${count.format(row.numerator)} ${labels.of} ${count.format(row.total)}`,
        percent.format(row.numerator / row.total),
      ]),
  });
  const basisRows = totals.map((t) => ({
    label: t.country,
    slug: t.slug,
    numerator: t.stating_their_basis,
    total: t.recommendations,
  }));
  const answeredRows = totals.map((t) => ({
    label: t.country,
    slug: t.slug,
    numerator: t.answered,
    total: t.recommendations,
  }));
  const chainRows = chain.map((c) => ({
    label: c.country,
    slug: c.slug,
    numerator: c.closed,
    total: c.recommendations,
  }));
  return (
    <div className="space-y-12">
      <PageIntro title={copy.jamforelse.title} lead={copy.jamforelse.lead} />
      <ChartSection
        title={labels.byYear.title}
        note={labels.byYear.note}
        tableLabel={labels.tableView}
        table={{
          headers: [labels.yearHeader, copy.jamforelse.table.recommendations],
          rows: years.map((y) => [y.year, count.format(y.recommendations)]),
        }}
      >
        <ColumnChart
          data={years.map((y) => ({
            label: String(y.year),
            value: y.recommendations,
          }))}
          format={(value) => count.format(value)}
        />
      </ChartSection>
      <ChartSection
        title={labels.basis.title}
        tableLabel={labels.tableView}
        table={shareTable(basisRows)}
      >
        <ShareBars
          rows={basisRows}
          locale={locale}
          hrefBase={hrefBase}
          ofWord={labels.of}
        />
      </ChartSection>
      <ChartSection
        title={labels.answered.title}
        tableLabel={labels.tableView}
        table={shareTable(answeredRows)}
      >
        <ShareBars
          rows={answeredRows}
          locale={locale}
          hrefBase={hrefBase}
          ofWord={labels.of}
        />
      </ChartSection>
      <ChartSection
        title={labels.chain.title}
        note={labels.chain.note}
        tableLabel={labels.tableView}
        table={shareTable(chainRows)}
      >
        <ShareBars
          rows={chainRows}
          locale={locale}
          hrefBase={hrefBase}
          ofWord={labels.of}
        />
      </ChartSection>
      <CountryTable
        totals={totals}
        labels={copy.jamforelse.table}
        locale={locale}
        hrefBase={hrefBase}
      />
      <aside className="max-w-2xl rounded-lg border border-border-soft bg-surface-raised p-4 text-sm">
        <h2 className="font-semibold">{copy.jamforelse.notShown.title}</h2>
        <p className="mt-1 text-ink-secondary">
          {copy.jamforelse.notShown.body}
        </p>
      </aside>
    </div>
  );
}

import Link from "next/link";
import type { Copy } from "@/content/types";
import type { CountryTotals } from "@/lib/underlag";

/**
 * The comparison in table form: always present, never an alternative that
 * has to be asked for. Shares sit next to the counts they are made of.
 */
export function CountryTable({
  totals,
  labels,
  locale,
  hrefBase,
}: {
  totals: CountryTotals[];
  labels: Copy["jamforelse"]["table"];
  locale: string;
  hrefBase: string;
}) {
  const count = new Intl.NumberFormat(locale);
  const percent = new Intl.NumberFormat(locale, {
    style: "percent",
    maximumFractionDigits: 0,
  });
  return (
    <div className="overflow-x-auto">
      <table className="w-full min-w-[36rem] border-collapse text-sm">
        <caption className="pb-3 text-left text-sm text-ink-secondary">
          {labels.caption}
        </caption>
        <thead>
          <tr className="border-b-2 border-ink text-left tablehead">
            <th scope="col" className="py-2 pr-4 font-semibold">
              {labels.country}
            </th>
            <th scope="col" className="py-2 pr-4 text-right font-semibold">
              {labels.audits}
            </th>
            <th scope="col" className="py-2 pr-4 text-right font-semibold">
              {labels.recommendations}
            </th>
            <th scope="col" className="py-2 pr-4 text-right font-semibold">
              {labels.shareBasis}
            </th>
            <th scope="col" className="py-2 text-right font-semibold">
              {labels.shareAnswered}
            </th>
          </tr>
        </thead>
        <tbody>
          {totals.map((row) => (
            <tr key={row.slug} className="border-b border-border-soft">
              <th scope="row" className="py-2 pr-4 text-left font-normal">
                <Link
                  href={`${hrefBase}${row.slug}/`}
                  className="text-ink underline underline-offset-2"
                >
                  {row.country}
                </Link>
              </th>
              <td className="py-2 pr-4 text-right tabular-nums">
                {count.format(row.audits)}
              </td>
              <td className="py-2 pr-4 text-right tabular-nums">
                {count.format(row.recommendations)}
              </td>
              <td className="py-2 pr-4 text-right tabular-nums">
                {percent.format(row.stating_their_basis / row.recommendations)}
                <span className="ml-1 text-xs text-ink-secondary">
                  ({count.format(row.stating_their_basis)})
                </span>
              </td>
              <td className="py-2 text-right tabular-nums">
                {percent.format(row.answered / row.recommendations)}
                <span className="ml-1 text-xs text-ink-secondary">
                  ({count.format(row.answered)})
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

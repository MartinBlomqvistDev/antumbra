import type { Metadata } from "next";
import { CountryTable } from "@/components/country-table";
import { PageIntro } from "@/components/shell";
import { sv } from "@/content/sv";
import { countryTotals, readCountryYears } from "@/lib/underlag";

export const metadata: Metadata = { title: sv.jamforelse.title };

export default function Jamforelse() {
  const totals = countryTotals(readCountryYears());
  return (
    <div className="space-y-10">
      <PageIntro title={sv.jamforelse.title} lead={sv.jamforelse.lead} />
      <CountryTable
        totals={totals}
        labels={sv.jamforelse.table}
        locale="sv-SE"
        hrefBase="/jamforelse/"
      />
      <aside className="max-w-2xl rounded-lg border border-border-soft bg-surface-raised p-4 text-sm">
        <h2 className="font-semibold">{sv.jamforelse.notShown.title}</h2>
        <p className="mt-1 text-ink-secondary">{sv.jamforelse.notShown.body}</p>
      </aside>
    </div>
  );
}

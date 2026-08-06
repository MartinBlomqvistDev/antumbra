import type { Metadata } from "next";
import { CountryTable } from "@/components/country-table";
import { PageIntro } from "@/components/shell";
import { en } from "@/content/en";
import { countryTotals, readCountryYears } from "@/lib/underlag";

export const metadata: Metadata = { title: en.jamforelse.title };

export default function Comparison() {
  const totals = countryTotals(readCountryYears());
  return (
    <div className="space-y-10">
      <PageIntro title={en.jamforelse.title} lead={en.jamforelse.lead} />
      <CountryTable
        totals={totals}
        labels={en.jamforelse.table}
        locale="en-GB"
        hrefBase="/en/jamforelse/"
      />
      <aside className="max-w-2xl rounded-lg border border-border-soft bg-surface-raised p-4 text-sm">
        <h2 className="font-semibold">{en.jamforelse.notShown.title}</h2>
        <p className="mt-1 text-ink-secondary">{en.jamforelse.notShown.body}</p>
      </aside>
    </div>
  );
}

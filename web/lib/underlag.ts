import { readFileSync, readdirSync } from "node:fs";
import { join } from "node:path";

/**
 * The per-country underlag written by pipeline/15_export_web_data.py: the
 * verbatim chain behind every number. The types mirror the export schema;
 * nothing is reshaped here, so what the page shows is what the pipeline
 * verified against the marts.
 */
export type Citation = {
  cites: string;
  number: number | null;
  resolved: boolean;
  kind: string | null;
  section: string | null;
  text: string | null;
};

export type MemberStateResponse = {
  response: string;
  plan_path: string;
  confirmed_by_text: boolean;
};

export type Recommendation = {
  number: number;
  text: string;
  legal_basis: string | null;
  states_its_basis: boolean;
  is_answered: boolean;
  answer_confirmed_by_text: boolean;
  citations: Citation[];
  responses: MemberStateResponse[];
};

export type AuditReport = {
  ref: string;
  year: number | null;
  title: string | null;
  report_path: string;
  sha256: string | null;
  recommendations: Recommendation[];
};

export type CountryUnderlag = {
  country: string;
  in_eu27: boolean;
  audits: AuditReport[];
};

export type CountryYearRow = {
  country: string;
  slug: string;
  in_eu27: boolean;
  audit_year: number | null;
  recommendations: number;
  audits: number;
  stating_their_basis: number;
  answered: number;
  confirmed: number;
  share_stating_their_basis: number;
  share_answered: number;
};

const dataDir = join(process.cwd(), "public", "data");

/** Every country slug with an underlag file, sorted. */
export function underlagSlugs(): string[] {
  return readdirSync(join(dataDir, "underlag"))
    .filter((name) => name.endsWith(".json"))
    .map((name) => name.slice(0, -".json".length))
    .sort();
}

/** Read one country's underlag at build time. */
export function readUnderlag(slug: string): CountryUnderlag {
  const path = join(dataDir, "underlag", `${slug}.json`);
  return JSON.parse(readFileSync(path, "utf-8")) as CountryUnderlag;
}

/** Read the verified country-by-year rows at build time. */
export function readCountryYears(): CountryYearRow[] {
  const path = join(dataDir, "country_year.json");
  return JSON.parse(readFileSync(path, "utf-8")) as CountryYearRow[];
}

/** Recommendations per audit year, summed over the EU countries. */
export function byYear(
  rows: CountryYearRow[],
): { year: number; recommendations: number }[] {
  const perYear = new Map<number, number>();
  for (const row of rows) {
    if (row.audit_year === null) continue;
    perYear.set(
      row.audit_year,
      (perYear.get(row.audit_year) ?? 0) + row.recommendations,
    );
  }
  return [...perYear.entries()]
    .map(([year, recommendations]) => ({ year, recommendations }))
    .sort((a, b) => a.year - b.year);
}

export type ChainClosure = {
  country: string;
  slug: string;
  recommendations: number;
  closed: number;
};

/**
 * How often the chain closes, per country, derived at build time from the
 * same verified underlag the country pages render: the recommendation
 * states its basis, at least one citation resolves to a paragraph, and at
 * least one member state response answers it (the mart_chain definition).
 */
export function chainClosureByCountry(): ChainClosure[] {
  return underlagSlugs()
    .map((slug) => {
      const underlag = readUnderlag(slug);
      let recommendations = 0;
      let closed = 0;
      for (const audit of underlag.audits) {
        for (const rec of audit.recommendations) {
          recommendations += 1;
          const resolves = rec.citations.some((c) => c.resolved);
          if (rec.states_its_basis && resolves && rec.responses.length > 0) {
            closed += 1;
          }
        }
      }
      return { country: underlag.country, slug, recommendations, closed };
    })
    .sort((a, b) => a.country.localeCompare(b.country, "en"));
}

export type CountryTotals = {
  country: string;
  slug: string;
  audits: number;
  recommendations: number;
  stating_their_basis: number;
  answered: number;
};

/** Sum the yearly rows per country; shares are derived where displayed. */
export function countryTotals(rows: CountryYearRow[]): CountryTotals[] {
  const bySlug = new Map<string, CountryTotals>();
  for (const row of rows) {
    const entry = bySlug.get(row.slug) ?? {
      country: row.country,
      slug: row.slug,
      audits: 0,
      recommendations: 0,
      stating_their_basis: 0,
      answered: 0,
    };
    entry.audits += row.audits;
    entry.recommendations += row.recommendations;
    entry.stating_their_basis += row.stating_their_basis;
    entry.answered += row.answered;
    bySlug.set(row.slug, entry);
  }
  return [...bySlug.values()].sort((a, b) =>
    a.country.localeCompare(b.country, "en"),
  );
}

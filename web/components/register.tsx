import { Fragment } from "react";
import type { RegisterAssociation, RegisterCell } from "@/lib/sverige";

type RegisterLabels = {
  species: Record<string, string>;
  categories: Record<"rutin" | "alla", string>;
  headers: { county: string; unannounced: string; deficiency: string; n: string };
  associations: {
    heading: string;
    headers: {
      species: string;
      year: string;
      category: string;
      counties: string;
      rho: string;
      p: string;
    };
  };
};

/**
 * The register extract, one table per species with the counties as rows and
 * the two years side by side. The unannounced share and the deficiency share
 * rest on different denominators, so each carries its own count beside it
 * rather than a shared one in the margin. Cattle opens by default because it
 * is the only species that carries the pre-registered test; the other three
 * are there, folded, so that nothing is held back.
 */
export function RegisterTables({
  cells,
  species,
  years,
  labels,
  locale,
}: {
  cells: RegisterCell[];
  species: string[];
  years: number[];
  labels: RegisterLabels;
  locale: string;
}) {
  const count = new Intl.NumberFormat(locale);
  const percent = new Intl.NumberFormat(locale, {
    style: "percent",
    maximumFractionDigits: 0,
  });
  const share = (value: number | null) =>
    value === null ? "" : percent.format(value);
  return (
    <div className="space-y-3">
      {species.map((animal, index) => {
        const own = cells.filter((cell) => cell.djurslag === animal);
        const counties = Array.from(new Set(own.map((cell) => cell.namn))).sort(
          (first, second) => first.localeCompare(second, locale),
        );
        return (
          <details
            key={animal}
            open={index === 0}
            className="border border-border-soft"
          >
            <summary className="cursor-pointer p-3 text-sm font-semibold">
              {labels.species[animal] ?? animal}
            </summary>
            <div className="overflow-x-auto border-t border-border-soft">
              <table className="w-full min-w-[46rem] border-collapse text-sm">
                <thead>
                  <tr className="border-b border-border-soft text-left tablehead">
                    <th
                      scope="col"
                      rowSpan={2}
                      className="px-3 py-1.5 align-bottom"
                    >
                      {labels.headers.county}
                    </th>
                    {years.map((year) => (
                      <th
                        key={year}
                        scope="colgroup"
                        colSpan={4}
                        className="px-3 py-1.5 text-left tabular-nums"
                      >
                        {year}
                      </th>
                    ))}
                  </tr>
                  <tr className="border-b border-border-soft text-left tablehead">
                    {years.map((year) => (
                      <Fragment key={year}>
                        <th scope="col" className="px-3 py-1.5 text-right">
                          {labels.headers.unannounced}
                        </th>
                        <th scope="col" className="py-1.5 pr-3 text-right">
                          {labels.headers.n}
                        </th>
                        <th scope="col" className="px-3 py-1.5 text-right">
                          {labels.headers.deficiency}
                        </th>
                        <th scope="col" className="py-1.5 pr-3 text-right">
                          {labels.headers.n}
                        </th>
                      </Fragment>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {counties.map((name) => (
                    <tr
                      key={name}
                      className="border-b border-border-soft align-top"
                    >
                      <td className="px-3 py-1.5">{name}</td>
                      {years.map((year) => {
                        const cell = own.find(
                          (candidate) =>
                            candidate.namn === name && candidate.ar === year,
                        );
                        const inspections =
                          cell &&
                          cell.aviserade !== null &&
                          cell.oaviserade !== null
                            ? cell.aviserade + cell.oaviserade
                            : null;
                        return (
                          <Fragment key={year}>
                            <td className="px-3 py-1.5 text-right tabular-nums">
                              {cell ? share(cell.andel_oanmalda) : ""}
                            </td>
                            <td className="py-1.5 pr-3 text-right tabular-nums text-ink-secondary">
                              {inspections === null
                                ? ""
                                : count.format(inspections)}
                            </td>
                            <td className="px-3 py-1.5 text-right tabular-nums">
                              {cell ? share(cell.rutin_andel) : ""}
                            </td>
                            <td className="py-1.5 pr-3 text-right tabular-nums text-ink-secondary">
                              {cell && cell.rutin_rader !== null
                                ? count.format(cell.rutin_rader)
                                : ""}
                            </td>
                          </Fragment>
                        );
                      })}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </details>
        );
      })}
    </div>
  );
}

/** The associations step 28 tested, exactly as the file carries them. */
export function AssociationTable({
  rows,
  labels,
  locale,
}: {
  rows: RegisterAssociation[];
  labels: RegisterLabels;
  locale: string;
}) {
  const three = new Intl.NumberFormat(locale, {
    minimumFractionDigits: 3,
    maximumFractionDigits: 3,
  });
  const four = new Intl.NumberFormat(locale, {
    minimumFractionDigits: 4,
    maximumFractionDigits: 4,
  });
  return (
    <div className="overflow-x-auto">
      <table className="w-full min-w-[34rem] border-collapse text-sm">
        <thead>
          <tr className="border-b border-border-soft text-left tablehead">
            <th scope="col" className="py-1.5 pr-4">
              {labels.associations.headers.species}
            </th>
            <th scope="col" className="py-1.5 pr-4">
              {labels.associations.headers.year}
            </th>
            <th scope="col" className="py-1.5 pr-4">
              {labels.associations.headers.category}
            </th>
            <th scope="col" className="py-1.5 pr-4 text-right">
              {labels.associations.headers.counties}
            </th>
            <th scope="col" className="py-1.5 pr-4 text-right">
              {labels.associations.headers.rho}
            </th>
            <th scope="col" className="py-1.5 text-right">
              {labels.associations.headers.p}
            </th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr
              key={`${row.djurslag}-${row.ar}-${row.kategori}`}
              className="border-b border-border-soft align-top"
            >
              <td className="py-1.5 pr-4">
                {labels.species[row.djurslag] ?? row.djurslag}
              </td>
              <td className="py-1.5 pr-4 tabular-nums">{row.ar}</td>
              <td className="py-1.5 pr-4">{labels.categories[row.kategori]}</td>
              <td className="py-1.5 pr-4 text-right tabular-nums">{row.lan}</td>
              <td className="py-1.5 pr-4 text-right tabular-nums">
                {three.format(row.rho)}
              </td>
              <td className="py-1.5 text-right tabular-nums">
                {four.format(row.p)}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

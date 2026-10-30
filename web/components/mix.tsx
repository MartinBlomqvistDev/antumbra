import { Fragment } from "react";
import type { MixAssociation, MixCounty } from "@/lib/sverige";

export type MixLabels = {
  axisX: string;
  axisY: string;
  line: string;
  chartLabel: string;
  dotTitle: string;
  summary: string;
  headers: {
    county: string;
    routine: string;
    unannounced: string;
    range: string;
    n: string;
  };
  rangeFormat: string;
  associations: {
    heading: string;
    note: string;
    headers: {
      measure: string;
      year: string;
      counties: string;
      rho: string;
      p: string;
    };
    measures: Record<string, string>;
  };
};

const SURFACE = "var(--surface)";
const INK = "var(--ink)";
const SECOND = "var(--ink-secondary)";
const BORDER = "var(--border)";
const DOT = "var(--accent)";

const WIDTH = 400;
const HEIGHT = 372;
const LEFT = 48;
const RIGHT = 382;
const TOP = 34;
const BOTTOM = 318;
const TICKS = [0, 0.25, 0.5, 0.75, 1];

function atX(share: number): number {
  return LEFT + (RIGHT - LEFT) * share;
}

function atY(share: number): number {
  return BOTTOM - (BOTTOM - TOP) * share;
}

/**
 * The counties worth a name in one panel: the lowest and highest unannounced
 * share, and the two furthest above the line, where routine inspections must
 * themselves have been unannounced. Naming all 21 would bury the pattern, and
 * the table under the chart carries every county.
 */
function named(rows: MixCounty[]): Set<string> {
  const byShare = [...rows].sort(
    (first, second) => first.andel_oanmalda - second.andel_oanmalda,
  );
  const above = [...rows].sort(
    (first, second) =>
      second.andel_oanmalda +
      second.andel_rutin -
      (first.andel_oanmalda + first.andel_rutin),
  );
  return new Set([
    byShare[0].namn,
    byShare[byShare.length - 1].namn,
    above[0].namn,
    above[1].namn,
  ]);
}

/** Whether another dot sits where this county's name would go beside its dot. */
function crowded(row: MixCounty, rows: MixCounty[], flip: boolean): boolean {
  const x = atX(1 - row.andel_rutin);
  const y = atY(row.andel_oanmalda);
  const length = row.namn.length * 6.6 + 8;
  return rows.some((other) => {
    if (other.slug === row.slug) {
      return false;
    }
    const dx = (atX(1 - other.andel_rutin) - x) * (flip ? -1 : 1);
    const dy = Math.abs(atY(other.andel_oanmalda) - y);
    return dx > 0 && dx < length && dy < 11;
  });
}

/**
 * One panel per year rather than a toggle, so the two years can be read side by
 * side and the chart needs no script. Position carries the whole comparison.
 * The dashed line is the reading aid: a county on it has exactly as many
 * unannounced inspections as inspections outside routine.
 */
function Panel({
  rows,
  year,
  labels,
  percent,
}: {
  rows: MixCounty[];
  year: number;
  labels: MixLabels;
  percent: Intl.NumberFormat;
}) {
  const names = named(rows);
  return (
    <svg
      viewBox={`0 0 ${WIDTH} ${HEIGHT}`}
      role="img"
      aria-label={labels.chartLabel.replace("{year}", String(year))}
      className="h-auto w-full"
    >
      <text x={LEFT} y={16} fontSize={14} fontWeight={600} fill={INK}>
        {year}
      </text>
      {TICKS.map((tick) => (
        <Fragment key={tick}>
          <line
            x1={LEFT}
            x2={RIGHT}
            y1={atY(tick)}
            y2={atY(tick)}
            stroke={BORDER}
            strokeWidth={0.5}
          />
          <line
            x1={atX(tick)}
            x2={atX(tick)}
            y1={TOP}
            y2={BOTTOM}
            stroke={BORDER}
            strokeWidth={0.5}
          />
          <text
            x={LEFT - 6}
            y={atY(tick) + 4}
            fontSize={11}
            textAnchor="end"
            fill={SECOND}
          >
            {percent.format(tick)}
          </text>
          <text
            x={atX(tick)}
            y={BOTTOM + 16}
            fontSize={11}
            textAnchor="middle"
            fill={SECOND}
          >
            {percent.format(tick)}
          </text>
        </Fragment>
      ))}
      <line
        x1={atX(0)}
        y1={atY(0)}
        x2={atX(1)}
        y2={atY(1)}
        stroke={SECOND}
        strokeWidth={1}
        strokeDasharray="4 4"
      />
      <text
        x={atX(0.8)}
        y={atY(0.94)}
        fontSize={11}
        textAnchor="end"
        fill={SECOND}
      >
        {labels.line}
      </text>
      {rows.map((row) => {
        const outside = 1 - row.andel_rutin;
        return (
          <circle
            key={row.slug}
            cx={atX(outside)}
            cy={atY(row.andel_oanmalda)}
            r={4.5}
            fill={DOT}
            stroke={SURFACE}
            strokeWidth={1.5}
          >
            <title>
              {labels.dotTitle
                .replace("{county}", row.namn)
                .replace("{outside}", percent.format(outside))
                .replace("{unannounced}", percent.format(row.andel_oanmalda))}
            </title>
          </circle>
        );
      })}
      {rows
        .filter((row) => names.has(row.namn))
        .map((row) => {
          const outside = 1 - row.andel_rutin;
          const flip = outside > 0.58;
          const lift = crowded(row, rows, flip);
          return (
            <text
              key={row.slug}
              x={atX(outside) + (flip ? -8 : 8)}
              y={atY(row.andel_oanmalda) + (lift ? -9 : 4)}
              fontSize={12}
              textAnchor={flip ? "end" : "start"}
              fill={INK}
              stroke={SURFACE}
              strokeWidth={3}
              paintOrder="stroke"
            >
              {row.namn}
            </text>
          );
        })}
      <text
        x={(LEFT + RIGHT) / 2}
        y={BOTTOM + 38}
        fontSize={12}
        textAnchor="middle"
        fill={SECOND}
      >
        {labels.axisX}
      </text>
      <text
        transform={`translate(13 ${(TOP + BOTTOM) / 2}) rotate(-90)`}
        fontSize={12}
        textAnchor="middle"
        fill={SECOND}
      >
        {labels.axisY}
      </text>
    </svg>
  );
}

export function MixChart({
  rows,
  years,
  labels,
  locale,
}: {
  rows: MixCounty[];
  years: number[];
  labels: MixLabels;
  locale: string;
}) {
  const percent = new Intl.NumberFormat(locale, {
    style: "percent",
    maximumFractionDigits: 0,
  });
  return (
    <div className="grid gap-4 md:grid-cols-2">
      {years.map((year) => (
        <Panel
          key={year}
          rows={rows.filter((row) => row.ar === year)}
          year={year}
          labels={labels}
          percent={percent}
        />
      ))}
    </div>
  );
}

/** Every county behind the chart, with the bounded share among routine inspections. */
export function MixTable({
  rows,
  years,
  labels,
  locale,
}: {
  rows: MixCounty[];
  years: number[];
  labels: MixLabels;
  locale: string;
}) {
  const percent = new Intl.NumberFormat(locale, {
    style: "percent",
    maximumFractionDigits: 0,
  });
  const whole = new Intl.NumberFormat(locale, { maximumFractionDigits: 0 });
  const count = new Intl.NumberFormat(locale);
  const counties = Array.from(new Set(rows.map((row) => row.namn))).sort(
    (first, second) => first.localeCompare(second, locale),
  );
  const range = (row: MixCounty) =>
    labels.rangeFormat
      .replace("{low}", whole.format(row.oanmalda_bland_rutin_min * 100))
      .replace("{high}", whole.format(row.oanmalda_bland_rutin_max * 100));
  return (
    <details className="border border-border-soft">
      <summary className="cursor-pointer p-3 text-sm font-semibold">
        {labels.summary}
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
                    {labels.headers.routine}
                  </th>
                  <th scope="col" className="px-3 py-1.5 text-right">
                    {labels.headers.unannounced}
                  </th>
                  <th scope="col" className="px-3 py-1.5 text-right">
                    {labels.headers.range}
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
              <tr key={name} className="border-b border-border-soft align-top">
                <td className="px-3 py-1.5">{name}</td>
                {years.map((year) => {
                  const row = rows.find(
                    (candidate) =>
                      candidate.namn === name && candidate.ar === year,
                  );
                  if (!row) {
                    return <td key={year} colSpan={4} />;
                  }
                  return (
                    <Fragment key={year}>
                      <td className="px-3 py-1.5 text-right tabular-nums">
                        {percent.format(row.andel_rutin)}
                      </td>
                      <td className="px-3 py-1.5 text-right tabular-nums">
                        {percent.format(row.andel_oanmalda)}
                      </td>
                      <td className="px-3 py-1.5 text-right tabular-nums">
                        {range(row)}
                      </td>
                      <td className="py-1.5 pr-3 text-right tabular-nums text-ink-secondary">
                        {count.format(row.aviserade + row.oaviserade)}
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
}

/** The exploratory associations, exactly as step 54 wrote them. */
export function MixAssociations({
  rows,
  labels,
  locale,
}: {
  rows: MixAssociation[];
  labels: MixLabels;
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
  const headers = labels.associations.headers;
  return (
    <div className="overflow-x-auto">
      <table className="w-full min-w-[34rem] border-collapse text-sm">
        <thead>
          <tr className="border-b border-border-soft text-left tablehead">
            <th scope="col" className="py-1.5 pr-4">
              {headers.measure}
            </th>
            <th scope="col" className="py-1.5 pr-4">
              {headers.year}
            </th>
            <th scope="col" className="py-1.5 pr-4 text-right">
              {headers.counties}
            </th>
            <th scope="col" className="py-1.5 pr-4 text-right">
              {headers.rho}
            </th>
            <th scope="col" className="py-1.5 text-right">
              {headers.p}
            </th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr
              key={`${row.matt}-${row.ar}`}
              className="border-b border-border-soft align-top"
            >
              <td className="py-1.5 pr-4">
                {labels.associations.measures[row.matt] ?? row.matt}
              </td>
              <td className="py-1.5 pr-4 tabular-nums">{row.ar}</td>
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

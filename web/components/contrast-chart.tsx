import type { RankingRow } from "@/lib/sverige";

/**
 * The contrast measure drawn once: one row per county that delivered in both
 * classes, the share of documents carrying at least one redaction in each.
 *
 * Why this form and not a map. The measure separates 39 of 136 county pairs in
 * class A, so for most counties it says nothing about which one redacts most. A
 * choropleth asserts a ranking in every pixel, louder than any caption can
 * withdraw it. A paired dot sorted by the gap puts the document type on the
 * axis the data supports, and the Wilson interval travels with the value rather
 * than in a footnote.
 */
export type ContrastLabels = {
  reports: string;
  decisions: string;
  countsNote: string;
  rowTitle: string;
};

const SURFACE = "var(--surface)";
const INK = "var(--ink)";
const SECOND = "var(--ink-secondary)";
const BORDER = "var(--border)";
const REPORTS = "var(--accent)";
const DECISIONS = "var(--accent-warm)";

const LEFT = 168;
const RIGHT = 648;
const TOP = 86;
const ROW = 27;
const WIDTH = 786;
const TICKS = [0, 0.25, 0.5, 0.75, 1];

/** The share's position on the axis. */
function at(share: number): number {
  return LEFT + (RIGHT - LEFT) * share;
}

/**
 * Four counties redact the same share in both classes, and a second dot drawn
 * at the same point is a dot a reader never sees. Where the two land within
 * one marker of each other they are nudged apart, so an equal row reads as two
 * marks that meet rather than as one class missing.
 */
function nudge(reports: number, decisions: number): number {
  return Math.abs(at(reports) - at(decisions)) < 12 ? 5.5 : 0;
}

export function ContrastChart({
  reports,
  decisions,
  labels,
}: {
  reports: RankingRow[];
  decisions: RankingRow[];
  labels: ContrastLabels;
}) {
  const bySlug = new Map(decisions.map((row) => [row.slug, row]));
  const rows = reports
    .filter((row) => bySlug.has(row.slug))
    .map((row) => ({ a: row, b: bySlug.get(row.slug)! }))
    .sort((first, second) => {
      const gap = (row: { a: RankingRow; b: RankingRow }) =>
        row.a.andel - row.b.andel;
      return (
        gap(second) - gap(first) ||
        first.a.namn.localeCompare(second.a.namn, "sv")
      );
    });
  const height = TOP + ROW * rows.length + 54;

  return (
    <svg
      viewBox={`0 0 ${WIDTH} ${height}`}
      className="h-auto w-full min-w-[46rem]"
      role="img"
      aria-labelledby="kontrast-titel kontrast-beskrivning"
    >
      <title id="kontrast-titel">{labels.countsNote}</title>
      <desc id="kontrast-beskrivning">
        {rows
          .map(({ a, b }) => `${a.namn}: ${a.andel_text} mot ${b.andel_text}`)
          .join(". ")}
      </desc>

      <circle cx={LEFT} cy={38} r={5.5} fill={REPORTS} />
      <text x={LEFT + 14} y={42} fontSize={15} fill={SECOND}>
        {labels.reports}
      </text>
      <circle cx={LEFT + 180} cy={38} r={5.5} fill={DECISIONS} />
      <text x={LEFT + 194} y={42} fontSize={15} fill={SECOND}>
        {labels.decisions}
      </text>

      {TICKS.map((tick) => (
        <g key={tick}>
          <line
            x1={at(tick)}
            y1={TOP - 18}
            x2={at(tick)}
            y2={TOP + ROW * rows.length - 8}
            stroke={BORDER}
            strokeWidth={1}
          />
          <text
            x={at(tick)}
            y={TOP - 26}
            textAnchor="middle"
            fontSize={12}
            fill={SECOND}
            className="font-mono"
          >
            {tick * 100} %
          </text>
        </g>
      ))}

      {rows.map(({ a, b }, index) => {
        const y = TOP + ROW * index;
        return (
          <g key={a.slug}>
            <title>
              {labels.rowTitle
                .replace("{county}", a.namn)
                .replace("{reports}", `${a.maskade}/${a.dokument}`)
                .replace("{reportsShare}", a.andel_text)
                .replace("{decisions}", `${b.maskade}/${b.dokument}`)
                .replace("{decisionsShare}", b.andel_text)}
            </title>
            <text
              x={LEFT - 16}
              y={y + 5}
              textAnchor="end"
              fontSize={15}
              fill={INK}
            >
              {a.namn}
            </text>
            {[b, a].map((row) => (
              <line
                key={`${row.slug}-${row.andel}`}
                x1={at(row.intervall[0])}
                y1={y}
                x2={at(row.intervall[1])}
                y2={y}
                stroke={BORDER}
                strokeWidth={3}
                strokeLinecap="round"
              />
            ))}
            <line
              x1={at(Math.min(a.andel, b.andel))}
              y1={y}
              x2={at(Math.max(a.andel, b.andel))}
              y2={y}
              stroke={INK}
              strokeWidth={1}
            />
            <circle
              cx={at(b.andel) - nudge(a.andel, b.andel)}
              cy={y}
              r={5.5}
              fill={DECISIONS}
              stroke={SURFACE}
              strokeWidth={2}
            />
            <circle
              cx={at(a.andel) + nudge(a.andel, b.andel)}
              cy={y}
              r={5.5}
              fill={REPORTS}
              stroke={SURFACE}
              strokeWidth={2}
            />
            <text
              x={RIGHT + 20}
              y={y + 4}
              fontSize={12}
              fill={SECOND}
              className="font-mono"
            >
              {a.maskade}/{a.dokument} · {b.maskade}/{b.dokument}
            </text>
          </g>
        );
      })}
    </svg>
  );
}

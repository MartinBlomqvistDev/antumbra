import Link from "next/link";

/**
 * The chart marks, built in plain SVG and HTML: thin bars, a recessive
 * grid, direct labels, native title tooltips, and a table view beside
 * every chart. Text wears text tokens; only the marks carry the accent.
 */

export function ColumnChart({
  data,
  tickEvery = 4,
  format,
}: {
  data: { label: string; value: number }[];
  tickEvery?: number;
  format: (value: number) => string;
}) {
  const width = 760;
  const height = 220;
  const pad = { top: 8, right: 4, bottom: 22, left: 40 };
  const innerWidth = width - pad.left - pad.right;
  const innerHeight = height - pad.top - pad.bottom;
  const max = Math.max(...data.map((d) => d.value));
  const scaleMax = Math.ceil(max / 100) * 100;
  const step = innerWidth / data.length;
  const barWidth = Math.max(step - 2, 2);
  const gridValues = [0.25, 0.5, 0.75, 1].map((share) => share * scaleMax);
  return (
    <svg
      viewBox={`0 0 ${width} ${height}`}
      role="img"
      className="w-full min-w-[36rem]"
    >
      {gridValues.map((value) => {
        const y = pad.top + innerHeight * (1 - value / scaleMax);
        return (
          <g key={value}>
            <line
              x1={pad.left}
              x2={width - pad.right}
              y1={y}
              y2={y}
              stroke="var(--border)"
              strokeWidth="1"
            />
            <text
              x={pad.left - 6}
              y={y + 3}
              textAnchor="end"
              fontSize="10"
              fill="var(--ink-secondary)"
            >
              {format(value)}
            </text>
          </g>
        );
      })}
      {data.map((d, index) => {
        const barHeight = innerHeight * (d.value / scaleMax);
        const x = pad.left + index * step;
        return (
          <g key={d.label}>
            <rect
              x={x}
              y={pad.top + innerHeight - barHeight}
              width={barWidth}
              height={barHeight}
              rx="2"
              fill="var(--accent)"
            >
              <title>{`${d.label}: ${format(d.value)}`}</title>
            </rect>
            {index % tickEvery === 0 ? (
              <text
                x={x + barWidth / 2}
                y={height - 6}
                textAnchor="middle"
                fontSize="10"
                fill="var(--ink-secondary)"
              >
                {d.label}
              </text>
            ) : null}
          </g>
        );
      })}
    </svg>
  );
}

export function ShareBars({
  rows,
  locale,
  hrefBase,
  ofWord,
}: {
  rows: { label: string; slug: string; numerator: number; total: number }[];
  locale: string;
  hrefBase: string;
  ofWord: string;
}) {
  const percent = new Intl.NumberFormat(locale, {
    style: "percent",
    maximumFractionDigits: 0,
  });
  const count = new Intl.NumberFormat(locale);
  const sorted = [...rows].sort(
    (a, b) => b.numerator / b.total - a.numerator / a.total,
  );
  return (
    <div className="space-y-1.5">
      {sorted.map((row) => {
        const share = row.numerator / row.total;
        return (
          <div
            key={row.slug}
            className="grid grid-cols-[9rem_1fr_auto] items-center gap-3 text-sm"
          >
            <Link
              href={`${hrefBase}${row.slug}/`}
              className="truncate underline underline-offset-2"
            >
              {row.label}
            </Link>
            <div
              className="h-3 "
              title={`${row.label}: ${percent.format(share)}`}
            >
              <div
                className="h-3 -sm bg-accent"
                style={{ width: `${Math.max(share * 100, 0.5)}%` }}
              />
            </div>
            <span className="tabular-nums text-xs text-ink-secondary">
              {percent.format(share)} ({count.format(row.numerator)} {ofWord}{" "}
              {count.format(row.total)})
            </span>
          </div>
        );
      })}
    </div>
  );
}

export function ChartSection({
  title,
  note,
  tableLabel,
  table,
  children,
}: {
  title: string;
  note?: string;
  tableLabel: string;
  table: { headers: string[]; rows: (string | number)[][] };
  children: React.ReactNode;
}) {
  return (
    <section className="space-y-3">
      <h2 className="text-2xl font-semibold tracking-tight">
        {title}
      </h2>
      {note ? (
        <p className="max-w-2xl text-sm text-ink-secondary">{note}</p>
      ) : null}
      <div className="overflow-x-auto">{children}</div>
      <details>
        <summary className="cursor-pointer text-sm text-ink-secondary">
          {tableLabel}
        </summary>
        <div className="mt-2 overflow-x-auto">
          <table className="min-w-[24rem] border-collapse text-sm">
            <thead>
              <tr className="border-b-2 border-ink text-left tablehead">
                {table.headers.map((header) => (
                  <th key={header} scope="col" className="py-1.5 pr-6">
                    {header}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {table.rows.map((cells, index) => (
                <tr key={index} className="border-b border-border-soft">
                  {cells.map((cell, cellIndex) => (
                    <td
                      key={cellIndex}
                      className={
                        cellIndex === 0
                          ? "py-1.5 pr-6"
                          : "py-1.5 pr-6 text-right tabular-nums"
                      }
                    >
                      {cell}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </details>
    </section>
  );
}

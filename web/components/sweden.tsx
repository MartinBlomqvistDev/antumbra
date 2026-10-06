import type { Authority, RankingRow, Reply } from "@/lib/sverige";

/**
 * The Swedish result surfaces: the comparison table for one class, and one
 * authority's own board with its reply beside its figures. Every word comes in
 * as a label, so the copy stays in the content files.
 */
export type ComparisonLabels = {
  caption: string;
  intervalNote: string;
  separated: string;
  headers: {
    place: string;
    authority: string;
    documents: string;
    share: string;
    interval: string;
  };
};

export type BoardLabels = {
  classWord: string;
  documents: string;
  masked: string;
  area: string;
  interval: string;
  place: string;
  placeOf: string;
  noFigures: string;
  reply: {
    heading: string;
    none: string;
    kinds: Record<Reply["typ"], string>;
    from: string;
    subject: string;
    attachments: string;
    omitted: string;
    message: string;
  };
  packet: { heading: string; note: string; sent: string };
};

export function ComparisonTable({
  rows,
  separatedPairs,
  pairs,
  labels,
  locale,
}: {
  rows: RankingRow[];
  separatedPairs: number;
  pairs: number;
  labels: ComparisonLabels;
  locale: string;
}) {
  const count = new Intl.NumberFormat(locale);
  return (
    <div className="space-y-2">
      <p className="max-w-2xl text-sm text-ink-secondary">{labels.caption}</p>
      <p className="max-w-2xl text-sm text-ink-secondary">
        {labels.intervalNote}{" "}
        {labels.separated
          .replace("{separated}", count.format(separatedPairs))
          .replace("{pairs}", count.format(pairs))}
      </p>
      <div className="overflow-x-auto">
        <table className="w-full min-w-[34rem] border-collapse text-sm">
          <thead>
            <tr className="border-b border-border-soft text-left uppercase tracking-wide text-ink-secondary">
              <th scope="col" className="py-1.5 pr-4">
                {labels.headers.place}
              </th>
              <th scope="col" className="py-1.5 pr-4">
                {labels.headers.authority}
              </th>
              <th scope="col" className="py-1.5 pr-4 text-right">
                {labels.headers.documents}
              </th>
              <th scope="col" className="py-1.5 pr-4 text-right">
                {labels.headers.share}
              </th>
              <th scope="col" className="py-1.5 text-right">
                {labels.headers.interval}
              </th>
            </tr>
          </thead>
          <tbody>
            {rows.map((row) => (
              <tr
                key={row.slug}
                className="border-b border-border-soft align-top"
              >
                <td className="py-1.5 pr-4 tabular-nums">{row.plats}</td>
                <td className="py-1.5 pr-4">{row.namn}</td>
                <td className="py-1.5 pr-4 text-right tabular-nums">
                  {count.format(row.dokument)}
                </td>
                <td className="py-1.5 pr-4 text-right tabular-nums">
                  {row.andel_text}
                </td>
                <td className="py-1.5 text-right tabular-nums text-ink-secondary">
                  {row.intervall_text}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export function AuthorityBoard({
  authority,
  labels,
  locale,
}: {
  authority: Authority;
  labels: BoardLabels;
  locale: string;
}) {
  const count = new Intl.NumberFormat(locale);
  const classes = Object.entries(authority.klasser);
  return (
    <details className="rounded-lg border border-border-soft bg-surface-raised">
      <summary className="cursor-pointer p-3 text-sm font-semibold">
        {authority.namn}
        <span className="ml-2 font-normal text-ink-secondary">
          {authority.svar_saknas
            ? labels.reply.none
            : labels.reply.kinds.substantiellt}
        </span>
      </summary>
      <div className="space-y-4 border-t border-border-soft p-3">
        {classes.length === 0 ? (
          <p className="text-sm text-ink-secondary">{labels.noFigures}</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full min-w-[32rem] border-collapse text-xs">
              <thead>
                <tr className="border-b border-border-soft text-left uppercase tracking-wide text-ink-secondary">
                  <th scope="col" className="py-1.5 pr-4">
                    {labels.classWord}
                  </th>
                  <th scope="col" className="py-1.5 pr-4 text-right">
                    {labels.documents}
                  </th>
                  <th scope="col" className="py-1.5 pr-4 text-right">
                    {labels.masked}
                  </th>
                  <th scope="col" className="py-1.5 pr-4 text-right">
                    {labels.interval}
                  </th>
                  <th scope="col" className="py-1.5 pr-4 text-right">
                    {labels.area}
                  </th>
                  <th scope="col" className="py-1.5 text-right">
                    {labels.place}
                  </th>
                </tr>
              </thead>
              <tbody>
                {classes.map(([klass, figures]) => (
                  <tr
                    key={klass}
                    className="border-b border-border-soft align-top"
                  >
                    <td className="py-1.5 pr-4">{klass}</td>
                    <td className="py-1.5 pr-4 text-right tabular-nums">
                      {count.format(figures.dokument)}
                    </td>
                    <td className="py-1.5 pr-4 text-right tabular-nums">
                      {count.format(figures.maskade)} ({figures.andel_text})
                    </td>
                    <td className="py-1.5 pr-4 text-right tabular-nums text-ink-secondary">
                      {figures.intervall_text}
                    </td>
                    <td className="py-1.5 pr-4 text-right tabular-nums">
                      {figures.yta_text}
                    </td>
                    <td className="py-1.5 text-right tabular-nums">
                      {authority.plats[klass as "A" | "B"]
                        ? `${authority.plats[klass as "A" | "B"]} ${labels.placeOf}`
                        : ""}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        <div className="space-y-3">
          <h3 className="text-sm font-semibold">{labels.reply.heading}</h3>
          {authority.svar.length === 0 ? (
            <p className="text-sm text-ink-secondary">{labels.reply.none}</p>
          ) : (
            authority.svar.map((reply) => (
              <div key={reply.meddelande} className="space-y-1 text-xs">
                <p className="text-ink-secondary">
                  {reply.datum} {reply.klockslag},{" "}
                  {labels.reply.kinds[reply.typ]}
                  {reply.roll ? `, ${labels.reply.from} ${reply.roll}` : ""}
                </p>
                <p className="text-ink-secondary">
                  {labels.reply.subject} {reply.amnesrad}
                </p>
                <pre className="overflow-x-auto whitespace-pre-wrap rounded border border-border-soft p-2 font-mono text-xs">
                  {reply.text}
                </pre>
                {reply.bilagor ? (
                  <p className="text-ink-secondary">
                    {labels.reply.attachments} {reply.bilagor}
                  </p>
                ) : null}
                {reply.utelamnat ? (
                  <p className="text-ink-secondary">
                    {labels.reply.omitted} {reply.utelamnat}
                  </p>
                ) : null}
                <p className="text-ink-secondary">
                  {labels.reply.message} {reply.meddelande}
                </p>
              </div>
            ))
          )}
        </div>

        {authority.paket ? (
          <div className="space-y-1 text-xs">
            <h3 className="text-sm font-semibold">{labels.packet.heading}</h3>
            <p className="text-ink-secondary">{labels.packet.note}</p>
            <p className="text-ink-secondary">
              {labels.packet.sent} {authority.paket.avsant}
            </p>
            <p>
              <code className="break-all">{authority.paket.sha256}</code>
            </p>
          </div>
        ) : null}
      </div>
    </details>
  );
}

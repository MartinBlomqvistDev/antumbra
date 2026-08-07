import type { Metadata } from "next";
import { EventLog } from "@/components/event-log";
import { PageIntro } from "@/components/shell";
import { sv } from "@/content/sv";
import { readAdrIndex, readLog } from "@/lib/log";

export const metadata: Metadata = { title: sv.metod.title };

export default function Metod() {
  const log = readLog();
  const adr = readAdrIndex();
  const count = new Intl.NumberFormat("sv-SE");
  const lastDate = log.reduce(
    (latest, row) => (row.datum > latest ? row.datum : latest),
    "",
  );
  return (
    <div className="space-y-12">
      <PageIntro title={sv.metod.title} lead={sv.metod.lead} />
      <section className="max-w-2xl space-y-2">
        <h2 className="font-display text-2xl font-semibold tracking-tight">
          {sv.metod.ai.heading}
        </h2>
        <p className="text-sm text-ink-secondary">{sv.metod.ai.body}</p>
      </section>
      <section className="max-w-2xl space-y-3">
        <h2 className="font-display text-2xl font-semibold tracking-tight">
          {sv.metod.adr.heading}
        </h2>
        <p className="text-sm text-ink-secondary">{sv.metod.adr.note}</p>
        <ol className="space-y-1 text-sm">
          {adr.map((entry) => (
            <li key={entry.id}>{entry.title}</li>
          ))}
        </ol>
      </section>
      <section className="space-y-3">
        <h2 className="font-display text-2xl font-semibold tracking-tight">
          {sv.metod.log.heading}
        </h2>
        <p className="max-w-2xl text-sm text-ink-secondary">
          {sv.metod.log.note} {count.format(log.length)}{" "}
          {sv.metod.log.countLabel} {lastDate}.
        </p>
        <EventLog rows={log} labels={sv.metod.log} />
      </section>
    </div>
  );
}

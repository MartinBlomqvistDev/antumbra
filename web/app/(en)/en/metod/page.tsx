import type { Metadata } from "next";
import { EventLog } from "@/components/event-log";
import { PageIntro } from "@/components/shell";
import { en } from "@/content/en";
import { readAdrIndex, readLog } from "@/lib/log";

export const metadata: Metadata = { title: en.metod.title };

export default function Method() {
  const log = readLog();
  const adr = readAdrIndex();
  const count = new Intl.NumberFormat("en-GB");
  const lastDate = log.reduce(
    (latest, row) => (row.datum > latest ? row.datum : latest),
    "",
  );
  return (
    <div className="space-y-12">
      <PageIntro title={en.metod.title} lead={en.metod.lead} />
      <section className="max-w-2xl space-y-3">
        <h2 className="font-display text-2xl font-semibold tracking-tight">
          {en.metod.avvikelser.heading}
        </h2>
        <p className="text-sm text-ink-secondary">
          {en.metod.avvikelser.note}
        </p>
        <dl className="space-y-3">
          {en.metod.avvikelser.items.map((item) => (
            <div key={item.title} className="space-y-1">
              <dt className="text-sm font-semibold">{item.title}</dt>
              <dd className="text-sm text-ink-secondary">{item.body}</dd>
            </div>
          ))}
        </dl>
      </section>
      <section className="max-w-2xl space-y-2">
        <h2 className="font-display text-2xl font-semibold tracking-tight">
          {en.metod.ai.heading}
        </h2>
        <p className="text-sm text-ink-secondary">{en.metod.ai.body}</p>
      </section>
      <section className="max-w-2xl space-y-3">
        <h2 className="font-display text-2xl font-semibold tracking-tight">
          {en.metod.adr.heading}
        </h2>
        <p className="text-sm text-ink-secondary">{en.metod.adr.note}</p>
        <ol className="space-y-1 text-sm">
          {adr.map((entry) => (
            <li key={entry.id}>{entry.title}</li>
          ))}
        </ol>
      </section>
      <section className="space-y-3">
        <h2 className="font-display text-2xl font-semibold tracking-tight">
          {en.metod.log.heading}
        </h2>
        <p className="max-w-2xl text-sm text-ink-secondary">
          {en.metod.log.note} {count.format(log.length)}{" "}
          {en.metod.log.countLabel} {lastDate}.
        </p>
        <EventLog rows={log} labels={en.metod.log} />
      </section>
    </div>
  );
}

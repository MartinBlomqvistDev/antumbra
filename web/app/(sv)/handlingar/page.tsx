import type { Metadata } from "next";
import { PageIntro } from "@/components/shell";
import { sv } from "@/content/sv";
import { readDeliveryManifest, readLog } from "@/lib/log";

const copy = sv.handlingar!;

export const metadata: Metadata = { title: copy.title };

export default function Handlingar() {
  const manifest = readDeliveryManifest();
  const log = readLog();
  const count = new Intl.NumberFormat("sv-SE");

  const feeStopped = [
    ...new Set(
      log
        .filter((row) => (row.notering ?? "").includes("avgiftsstoppad"))
        .map((row) => `${row.myndighet} · ${row.begaran}`),
    ),
  ].sort();

  const folders = new Map<string, typeof manifest>();
  for (const row of manifest) {
    const folder = row.path.split("/")[0];
    folders.set(folder, [...(folders.get(folder) ?? []), row]);
  }

  return (
    <div className="space-y-12">
      <PageIntro title={copy.title} lead={copy.lead} />
      <section className="max-w-2xl space-y-3">
        <h2 className="font-display text-2xl font-semibold tracking-tight">
          {copy.feeStopped.heading}
        </h2>
        <p className="text-sm text-ink-secondary">{copy.feeStopped.note}</p>
        <ul className="space-y-1 text-sm">
          {feeStopped.map((entry) => (
            <li key={entry}>{entry}</li>
          ))}
        </ul>
      </section>
      <section className="space-y-3">
        <h2 className="font-display text-2xl font-semibold tracking-tight">
          {copy.deliveries.heading}
        </h2>
        <p className="max-w-2xl text-sm text-ink-secondary">
          {copy.deliveries.note}
        </p>
        <div className="space-y-2">
          {[...folders.entries()]
            .sort(([a], [b]) => a.localeCompare(b, "sv"))
            .map(([folder, rows]) => (
              <details
                key={folder}
                className="rounded-lg border border-border-soft bg-surface-raised"
              >
                <summary className="cursor-pointer p-3 text-sm font-semibold">
                  {folder}
                  <span className="ml-2 font-normal text-ink-secondary">
                    {count.format(rows.length)} {copy.deliveries.filesWord}
                  </span>
                </summary>
                <div className="overflow-x-auto border-t border-border-soft p-3">
                  <table className="w-full min-w-[40rem] border-collapse text-xs">
                    <thead>
                      <tr className="border-b border-border-soft text-left uppercase tracking-wide text-ink-secondary">
                        <th scope="col" className="py-1.5 pr-4">
                          {copy.deliveries.headers.file}
                        </th>
                        <th scope="col" className="py-1.5 pr-4 text-right">
                          {copy.deliveries.headers.bytes}
                        </th>
                        <th scope="col" className="py-1.5">
                          {copy.deliveries.headers.sha256}
                        </th>
                      </tr>
                    </thead>
                    <tbody>
                      {rows.map((row) => (
                        <tr
                          key={row.path}
                          className="border-b border-border-soft align-top"
                        >
                          <td className="py-1.5 pr-4">
                            {row.path.split("/").slice(1).join("/")}
                          </td>
                          <td className="py-1.5 pr-4 text-right tabular-nums">
                            {count.format(row.bytes)}
                          </td>
                          <td className="py-1.5">
                            <code className="break-all">{row.sha256}</code>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </details>
            ))}
        </div>
      </section>
    </div>
  );
}

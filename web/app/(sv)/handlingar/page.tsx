import type { Metadata } from "next";
import { PageIntro } from "@/components/shell";
import { AuthorityBoard } from "@/components/sweden";
import { sv } from "@/content/sv";
import { readDeliveryManifest } from "@/lib/log";
import { readSweden } from "@/lib/sverige";

const copy = sv.handlingar!;

export const metadata: Metadata = { title: copy.title };

export default function Handlingar() {
  const manifest = readDeliveryManifest();
  const sweden = readSweden();
  const count = new Intl.NumberFormat("sv-SE");

  const folders = new Map<string, typeof manifest>();
  for (const row of manifest) {
    const folder = row.path.split("/")[0];
    folders.set(folder, [...(folders.get(folder) ?? []), row]);
  }

  return (
    <div className="space-y-12">
      <PageIntro title={copy.title} lead={copy.lead} />
      <section className="space-y-3">
        <h2 className="text-2xl font-semibold tracking-tight">
          {copy.tavla.heading}
        </h2>
        <p className="max-w-2xl text-sm text-ink-secondary">
          {copy.tavla.note}
        </p>
        <div className="space-y-2">
          {sweden.myndigheter.map((authority) => (
            <AuthorityBoard
              key={authority.slug}
              authority={authority}
              labels={copy.tavla}
              locale="sv-SE"
            />
          ))}
        </div>
      </section>
      <section className="space-y-3">
        <h2 className="text-2xl font-semibold tracking-tight">
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
                className="-lg border border-border-soft"
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
                      <tr className="border-b border-border-soft text-left fieldname">
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

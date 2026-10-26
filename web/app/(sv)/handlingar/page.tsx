import type { Metadata } from "next";
import { PageIntro } from "@/components/shell";
import { AuthorityBoard, CourtBoard } from "@/components/sweden";
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
  // The two measured classes first under each authority, then everything else
  // that arrived in the same cases: fee decisions, refusals, court
  // correspondence. Plain alphabetical order put kalmar_B after
  // kalmar_avslagsbeslut, which reads as a list that lost its order.
  const rank = (folder: string) => {
    const suffix = folder.slice(folder.lastIndexOf("_") + 1);
    return suffix === "A" ? 0 : suffix === "B" ? 1 : 2;
  };
  const order = ([a]: [string, unknown], [b]: [string, unknown]) => {
    const stemA = a.slice(0, a.lastIndexOf("_"));
    const stemB = b.slice(0, b.lastIndexOf("_"));
    return (
      stemA.localeCompare(stemB, "sv") ||
      rank(a) - rank(b) ||
      a.localeCompare(b, "sv")
    );
  };

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
          {copy.domstolar.heading}
        </h2>
        <p className="max-w-2xl text-sm text-ink-secondary">
          {copy.domstolar.note}
        </p>
        <div className="space-y-2">
          {sweden.domstolar.map((court) => (
            <CourtBoard
              key={court.myndighet}
              court={court}
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
            .sort(order)
            .map(([folder, rows]) => (
              <details
                key={folder}
                className="border border-border-soft"
              >
                <summary className="cursor-pointer p-3 text-sm font-semibold">
                  {folder}{" "}
                  <span className="font-normal text-ink-secondary">
                    {count.format(rows.length)}{" "}
                    {rows.length === 1
                      ? copy.deliveries.fileWord
                      : copy.deliveries.filesWord}
                  </span>
                </summary>
                <div className="overflow-x-auto border-t border-border-soft p-3">
                  <table className="w-full min-w-[40rem] border-collapse text-xs">
                    <thead>
                      <tr className="border-b border-border-soft text-left tablehead">
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

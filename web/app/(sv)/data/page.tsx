import type { Metadata } from "next";
import { PageIntro } from "@/components/shell";
import { sv } from "@/content/sv";
import { readDataset } from "@/lib/datasets";

const copy = sv.data!;

export const metadata: Metadata = { title: copy.title };

export default function DataPage() {
  const count = new Intl.NumberFormat("sv-SE");
  return (
    <div className="space-y-12">
      <PageIntro title={copy.title} lead={copy.lead} />
      <p className="max-w-2xl text-sm text-ink-secondary">{copy.note}</p>
      {copy.groups.map((group) => (
        <section key={group.heading} className="space-y-3">
          <h2 className="font-display text-2xl font-semibold tracking-tight">
            {group.heading}
          </h2>
          <p className="max-w-2xl text-sm text-ink-secondary">{group.note}</p>
          <div className="overflow-x-auto">
            <table className="w-full min-w-[46rem] border-collapse text-sm">
              <thead>
                <tr className="border-b border-border-soft text-left uppercase tracking-wide text-ink-secondary">
                  <th scope="col" className="py-1.5 pr-4">
                    {copy.headers.file}
                  </th>
                  <th scope="col" className="py-1.5 pr-4 text-right">
                    {copy.headers.rows}
                  </th>
                  <th scope="col" className="py-1.5 pr-4 text-right">
                    {copy.headers.bytes}
                  </th>
                  <th scope="col" className="py-1.5">
                    {copy.headers.description}
                  </th>
                </tr>
              </thead>
              <tbody>
                {group.files.map((file) => {
                  const measured = readDataset(file.path);
                  return (
                    <tr
                      key={file.path}
                      className="border-b border-border-soft align-top"
                    >
                      <td className="py-1.5 pr-4">
                        <code>{file.path.replace("data/", "")}</code>
                      </td>
                      <td className="py-1.5 pr-4 text-right tabular-nums">
                        {measured ? count.format(measured.rows) : ""}
                      </td>
                      <td className="py-1.5 pr-4 text-right tabular-nums">
                        {measured ? count.format(measured.bytes) : ""}
                      </td>
                      <td className="py-1.5 text-ink-secondary">
                        {measured
                          ? file.beskrivning
                          : `${file.beskrivning} (${copy.missing})`}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </section>
      ))}
      <section className="max-w-2xl space-y-2">
        <h2 className="font-display text-2xl font-semibold tracking-tight">
          {copy.licence.heading}
        </h2>
        <p className="text-sm text-ink-secondary">{copy.licence.body}</p>
      </section>
    </div>
  );
}

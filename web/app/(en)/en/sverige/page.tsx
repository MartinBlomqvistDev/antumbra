import type { Metadata } from "next";
import Link from "next/link";
import { PageIntro } from "@/components/shell";
import { ContrastChart } from "@/components/contrast-chart";
import { MixAssociations, MixChart, MixTable } from "@/components/mix";
import { AssociationTable, RegisterTables } from "@/components/register";
import { ComparisonTable } from "@/components/sweden";
import { en } from "@/content/en";
import { swedenStats } from "@/lib/stats";
import { mixBounds, mixSwing, readSweden } from "@/lib/sverige";

const copy = en.sverige!;

const LOCALE = "en-GB";

const CLASSES = ["A", "B"] as const;

export const metadata: Metadata = { title: copy.title };

export default function Sweden() {
  const stats = swedenStats();
  const count = new Intl.NumberFormat(LOCALE);
  const sweden = readSweden();
  const points = new Intl.NumberFormat(LOCALE, {
    minimumFractionDigits: 1,
    maximumFractionDigits: 1,
  });
  // The area difference is a tenth of the document difference, so one decimal
  // would print two counties apart as the same number.
  const area = new Intl.NumberFormat(LOCALE, {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });
  const pair = sweden.par.lan[0];
  const pairFinding = pair
    ? copy.par.finding
        .replace("{county}", pair.namn)
        .replace("{counties}", count.format(sweden.par.lan_med_nummer_i_bada))
        .replace("{pairs}", count.format(pair.par))
        .replace("{maskedA}", count.format(pair.maskade_a))
        .replace("{documentsA}", count.format(pair.dokument_a))
        .replace("{maskedB}", count.format(pair.maskade_b))
        .replace("{documentsB}", count.format(pair.dokument_b))
    : "";
  const pairLimit = copy.par.limit
    .replace("{unnumbered}", count.format(sweden.par.utan_arendenummer))
    .replace("{files}", count.format(sweden.par.filer));
  const annexFinding = copy.bilagor.finding
    .replace("{files}", count.format(sweden.bilagor.bilagefiler))
    .replace("{counties}", count.format(sweden.bilagor.lan_med_bilagefil))
    .replace("{refers}", count.format(sweden.bilagor.hanvisar_till_innehall))
    .replace(
      "{template}",
      count.format(sweden.bilagor.slag["fotomening ur mallen"] ?? 0),
    );
  const contrast = copy.resultat.contrast
    .replace("{counties}", count.format(sweden.kontrast.lan))
    .replace(
      "{share}",
      points.format(sweden.kontrast.median_dokumentandel ?? 0),
    )
    .replace("{area}", area.format(sweden.kontrast.median_yta ?? 0));
  const exception =
    sweden.kontrast.hogre_dokumentandel_i_b.length > 0
      ? copy.resultat.contrastException.replace(
          "{names}",
          new Intl.ListFormat(LOCALE).format(
            sweden.kontrast.hogre_dokumentandel_i_b,
          ),
        )
      : copy.resultat.contrastNoException;
  const overview = [
    { value: count.format(stats.sent), label: copy.overview.sent },
    { value: count.format(stats.files), label: copy.overview.files },
    {
      value: count.format(stats.deliveringAuthorities),
      label: copy.overview.deliveringAuthorities,
    },
    {
      value: count.format(stats.feeNotices),
      label: copy.overview.feeNotices,
    },
    {
      value: count.format(stats.feeStopped.length),
      label: copy.overview.feeStopped,
    },
    { value: copy.overview.paidValue, label: copy.overview.paid },
  ];
  return (
    <div className="space-y-12">
      <PageIntro title={copy.title} lead={copy.lead} />
      <section className="max-w-2xl space-y-2">
        <h2 className="text-2xl font-semibold tracking-tight">
          {copy.design.heading}
        </h2>
        <p className="text-sm text-ink-secondary">{copy.design.body}</p>
        <p className="text-sm text-ink-secondary">{copy.processNote}</p>
      </section>
      <section className="space-y-3">
        <h2 className="text-2xl font-semibold tracking-tight">
          {copy.overview.heading}
        </h2>
        <dl className="divide-y divide-border-soft border-y border-border-soft">
          {overview.map((item) => (
            <div
              key={item.label}
              className="grid items-baseline gap-x-6 py-3 sm:grid-cols-[9rem_1fr]"
            >
              <dd className="text-2xl font-semibold tabular-nums tracking-tight">
                {item.value}
              </dd>
              <dt className="text-ink-secondary">{item.label}</dt>
            </div>
          ))}
        </dl>
        <p className="text-sm text-ink-secondary">
          <Link
            href="/handlingar/"
            className="text-ink underline underline-offset-2"
          >
            {copy.toHandlingar}
          </Link>
        </p>
      </section>
      <section className="space-y-3">
        <h2 className="text-2xl font-semibold tracking-tight">
          {copy.resultat.heading}
        </h2>
        <p className="max-w-2xl text-sm text-ink-secondary">
          {copy.resultat.note}
        </p>
        <div className="overflow-x-auto">
          <table className="w-full min-w-[32rem] border-collapse text-sm">
            <thead>
              <tr className="border-b border-border-soft text-left tablehead">
                <th scope="col" className="py-1.5 pr-4">
                  {copy.resultat.classLabel}
                </th>
                <th scope="col" className="py-1.5 pr-4 text-right">
                  {copy.resultat.documents}
                </th>
                <th scope="col" className="py-1.5 pr-4 text-right">
                  {copy.resultat.masked}
                </th>
                <th scope="col" className="py-1.5 text-right">
                  {copy.resultat.authorities}
                </th>
              </tr>
            </thead>
            <tbody>
              {CLASSES.map((klass) => (
                <tr key={klass} className="border-b border-border-soft">
                  <td className="py-1.5 pr-4">
                    {copy.resultat.classes[klass]}
                  </td>
                  <td className="py-1.5 pr-4 text-right tabular-nums">
                    {count.format(sweden.klasser[klass].dokument)}
                  </td>
                  <td className="py-1.5 pr-4 text-right tabular-nums">
                    {count.format(sweden.klasser[klass].maskade)} (
                    {sweden.klasser[klass].andel_text})
                  </td>
                  <td className="py-1.5 text-right tabular-nums">
                    {count.format(sweden.klasser[klass].myndigheter)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <p className="max-w-2xl text-sm text-ink-secondary">{contrast}</p>
        <p className="max-w-2xl text-sm text-ink-secondary">{exception}</p>
      </section>
      <section className="space-y-3">
        <h2 className="text-2xl font-semibold tracking-tight">
          {copy.kontrastDiagram.heading}
        </h2>
        <p className="max-w-2xl text-sm text-ink-secondary">
          {copy.kontrastDiagram.note}
        </p>
        <div className="overflow-x-auto">
          <ContrastChart
            reports={sweden.jamforelse.A.rader}
            decisions={sweden.jamforelse.B.rader}
            labels={copy.kontrastDiagram}
          />
        </div>
        <p className="max-w-2xl text-sm text-ink-secondary">
          {copy.kontrastDiagram.limit}
        </p>
      </section>
      <section className="space-y-6">
        <h2 className="text-2xl font-semibold tracking-tight">
          {copy.lanJamforelse.heading}
        </h2>
        <p className="max-w-2xl text-sm text-ink-secondary">
          {copy.lanJamforelse.note}
        </p>
        {CLASSES.map((klass) => (
          <div key={klass} className="space-y-2">
            <h3 className="text-xl font-semibold tracking-tight">
              {copy.lanJamforelse.classHeading[klass]}
            </h3>
            <ComparisonTable
              rows={sweden.jamforelse[klass].rader}
              separatedPairs={sweden.jamforelse[klass].atskilda_par}
              pairs={sweden.jamforelse[klass].par}
              labels={copy.lanJamforelse}
              locale={LOCALE}
            />
          </div>
        ))}
      </section>
      <section className="max-w-2xl space-y-2">
        <h2 className="text-2xl font-semibold tracking-tight">
          {copy.par.heading}
        </h2>
        <p className="text-sm text-ink-secondary">{copy.par.note}</p>
        <p className="text-sm">{pairFinding}</p>
        <p className="text-sm text-ink-secondary">{pairLimit}</p>
      </section>
      <section className="max-w-2xl space-y-2">
        <h2 className="text-2xl font-semibold tracking-tight">
          {copy.bilagor.heading}
        </h2>
        <p className="text-sm text-ink-secondary">{copy.bilagor.note}</p>
        <p className="text-sm">{annexFinding}</p>
        <p className="text-sm text-ink-secondary">
          {copy.bilagor.limit.replace(
            "{unreadable}",
            count.format(sweden.bilagor.utan_lasbar_text),
          )}
        </p>
      </section>
      <section className="space-y-3">
        <h2 className="text-2xl font-semibold tracking-tight">
          {copy.register.heading}
        </h2>
        <p className="max-w-2xl text-sm">{copy.register.lead}</p>
        <p className="max-w-2xl text-sm text-ink-secondary">
          {copy.register.note.replace(
            "{reports}",
            count.format(sweden.register.rapporter),
          )}
        </p>
        <p className="max-w-2xl text-sm text-ink-secondary">
          {copy.register.reading}
        </p>
        <h3 className="pt-2 text-base font-semibold">
          {copy.register.mix.heading}
        </h3>
        <p className="max-w-2xl text-sm text-ink-secondary">
          {copy.register.mix.reading}
        </p>
        <MixChart
          rows={sweden.register.mix.lan}
          years={sweden.register.ar}
          labels={copy.register.mix}
          locale={LOCALE}
        />
        <p className="max-w-2xl text-sm">
          {mixSwing(copy.register.mix.swing, sweden, LOCALE)}
        </p>
        <p className="max-w-2xl text-sm text-ink-secondary">
          {mixBounds(copy.register.mix.bounds, sweden)}
        </p>
        <MixTable
          rows={sweden.register.mix.lan}
          years={sweden.register.ar}
          labels={copy.register.mix}
          locale={LOCALE}
        />
        <p className="max-w-2xl text-sm text-ink-secondary">
          {copy.register.mix.direction}
        </p>
        <h3 className="pt-2 text-base font-semibold">
          {copy.register.mix.associations.heading}
        </h3>
        <p className="max-w-2xl text-sm text-ink-secondary">
          {copy.register.mix.associations.note}
        </p>
        <MixAssociations
          rows={sweden.register.mix.samband}
          labels={copy.register.mix}
          locale={LOCALE}
        />
        <h3 className="pt-2 text-base font-semibold">
          {copy.register.tablesHeading}
        </h3>
        <RegisterTables
          cells={sweden.register.celler}
          species={sweden.register.djurslag}
          years={sweden.register.ar}
          labels={copy.register}
          locale={LOCALE}
        />
        <h3 className="pt-2 text-base font-semibold">
          {copy.register.associations.heading}
        </h3>
        <p className="max-w-2xl text-sm text-ink-secondary">
          {copy.register.hypothesis}
        </p>
        <AssociationTable
          rows={sweden.register.samband}
          labels={copy.register}
          locale={LOCALE}
        />
        <p className="max-w-2xl text-sm">{copy.register.outcome}</p>
        <ul className="max-w-2xl list-disc space-y-1 pl-5 text-sm text-ink-secondary">
          {copy.register.limits.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      </section>
      <section className="max-w-2xl space-y-3">
        <h2 className="text-2xl font-semibold tracking-tight">
          {copy.wordings.heading}
        </h2>
        <p className="text-sm text-ink-secondary">{copy.wordings.note}</p>
        <div className="space-y-2">
          {copy.wordings.items.map((item) => (
            <details key={item.label} className="border border-border-soft">
              <summary className="cursor-pointer p-3 text-sm font-semibold">
                {item.label}
              </summary>
              <p
                lang="sv"
                className="whitespace-pre-line border-t border-border-soft p-4 text-sm"
              >
                {item.text}
              </p>
            </details>
          ))}
        </div>
      </section>
      <section className="max-w-2xl space-y-3">
        <h2 className="text-2xl font-semibold tracking-tight">
          {copy.feeStopped.heading}
        </h2>
        <p className="text-sm text-ink-secondary">{copy.feeStopped.note}</p>
        <ul className="space-y-1 text-sm">
          {stats.feeStopped.map((entry) => {
            // Whether that class later arrived anyway, read from the figures
            // rather than stated here: one county's fee fell away after the
            // waiver and its documents came in, and a list that left that out
            // would read as four counties that released nothing.
            const delivered = Boolean(
              sweden.myndigheter.find(
                (item) => item.myndighet === entry.authority,
              )?.klasser[entry.request as "A" | "B"],
            );
            return (
              <li key={`${entry.authority} ${entry.request}`}>
                <span lang="sv">{entry.authority}</span> · {entry.request} ·{" "}
                <span className="text-ink-secondary">
                  {delivered
                    ? copy.feeStopped.laterDelivered
                    : copy.feeStopped.noCopies}
                </span>
              </li>
            );
          })}
        </ul>
      </section>
      <section className="max-w-2xl space-y-2">
        <h2 className="text-2xl font-semibold tracking-tight">
          {copy.notShown.heading}
        </h2>
        <ul className="list-disc space-y-1 pl-5 text-sm text-ink-secondary">
          {copy.notShown.items.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      </section>
    </div>
  );
}

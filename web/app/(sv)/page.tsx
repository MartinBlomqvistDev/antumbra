import { ChainExample } from "@/components/chain-example";
import { FigureTable } from "@/components/shell";
import { sv } from "@/content/sv";
import { readHeadline } from "@/lib/data";
import { readSweden } from "@/lib/sverige";

export default function Home() {
  const headline = readHeadline();
  const sverige = readSweden();
  const count = new Intl.NumberFormat("sv-SE");
  const percent = new Intl.NumberFormat("sv-SE", {
    style: "percent",
    maximumFractionDigits: 1,
  });
  // The finding first: the same kind of information, under the same
  // provision, released in one class and redacted in the other. The figures
  // are read from the export, never typed in here.
  const classLabel = (template: string, klass: "A" | "B") =>
    template
      .replace("{dokument}", count.format(sverige.klasser[klass].dokument))
      .replace("{lan}", count.format(sverige.klasser[klass].myndigheter));
  const sweden = [
    {
      value: percent.format(sverige.klasser.A.andel),
      label: classLabel(sv.home.swedenLabels!.classA, "A"),
    },
    {
      value: percent.format(sverige.klasser.B.andel),
      label: classLabel(sv.home.swedenLabels!.classB, "B"),
    },
    {
      value: sv.home.swedenLabels!.paidValue,
      label: sv.home.swedenLabels!.paid,
    },
  ];
  const eu = [
    { value: count.format(headline.audits), label: sv.home.numberLabels.audits },
    {
      value: count.format(headline.recommendations),
      label: sv.home.numberLabels.recommendations,
    },
    {
      value: percent.format(headline.share_citations_resolved),
      label: sv.home.numberLabels.citationsResolved,
    },
  ];
  return (
    <div className="space-y-14">
      <div className="max-w-[34rem] space-y-5">
        <p className="fieldname">{sv.home.kicker}</p>
        <h1 className="text-[2.6rem] font-semibold leading-[1.1] tracking-tight sm:text-5xl">
          {sv.site.tagline}
        </h1>
        <p className="text-lg text-ink-secondary">{sv.home.lead}</p>
      </div>
      <FigureTable
        caption={sv.home.swedenHeading!}
        rows={sweden}
        href="/sverige/"
      />
      <FigureTable
        caption={sv.home.euHeading!}
        rows={eu}
        href="/jamforelse/"
      />
      <ChainExample copy={sv} locale="sv-SE" hrefBase="/jamforelse/" />
    </div>
  );
}

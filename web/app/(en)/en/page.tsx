import { ChainExample } from "@/components/chain-example";
import { FigureTable } from "@/components/shell";
import { en } from "@/content/en";
import { readHeadline } from "@/lib/data";
import { readSweden } from "@/lib/sverige";

export default function Home() {
  const headline = readHeadline();
  const sverige = readSweden();
  const count = new Intl.NumberFormat("en-GB");
  const percent = new Intl.NumberFormat("en-GB", {
    style: "percent",
    maximumFractionDigits: 1,
  });
  // Same order as the Swedish page: the finding first, read from the export.
  const classLabel = (template: string, klass: "A" | "B") =>
    template
      .replace("{dokument}", count.format(sverige.klasser[klass].dokument))
      .replace("{lan}", count.format(sverige.klasser[klass].myndigheter));
  const sweden = [
    {
      value: percent.format(sverige.klasser.A.andel),
      label: classLabel(en.home.swedenLabels!.classA, "A"),
    },
    {
      value: percent.format(sverige.klasser.B.andel),
      label: classLabel(en.home.swedenLabels!.classB, "B"),
    },
    {
      value: en.home.swedenLabels!.paidValue,
      label: en.home.swedenLabels!.paid,
    },
  ];
  const eu = [
    { value: count.format(headline.audits), label: en.home.numberLabels.audits },
    {
      value: count.format(headline.recommendations),
      label: en.home.numberLabels.recommendations,
    },
    {
      value: percent.format(headline.share_citations_resolved),
      label: en.home.numberLabels.citationsResolved,
    },
  ];
  return (
    <div className="space-y-14">
      <div className="max-w-[34rem] space-y-5">
        <h1 className="text-[2.6rem] font-semibold leading-[1.15] tracking-tight sm:text-[3.1rem]">
          {en.home.kicker}
        </h1>
        <p className="text-lg text-ink-secondary">{en.home.lead}</p>
      </div>
      <FigureTable
        caption={en.home.swedenHeading!}
        rows={sweden}
        href="/en/sverige/"
      />
      <FigureTable
        caption={en.home.euHeading!}
        rows={eu}
        href="/en/jamforelse/"
      />
      <ChainExample copy={en} locale="en-GB" hrefBase="/en/jamforelse/" />
    </div>
  );
}

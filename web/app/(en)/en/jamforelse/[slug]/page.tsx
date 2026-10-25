import type { Metadata } from "next";
import Link from "next/link";
import { ChainAudit } from "@/components/chain";
import { en } from "@/content/en";
import { readUnderlag, underlagSlugs } from "@/lib/underlag";

export function generateStaticParams() {
  return underlagSlugs().map((slug) => ({ slug }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  return { title: readUnderlag(slug).country };
}

export default async function Country({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const underlag = readUnderlag(slug);
  const count = new Intl.NumberFormat("en-GB");
  const audits = [...underlag.audits].sort(
    (a, b) => (b.year ?? 0) - (a.year ?? 0) || a.ref.localeCompare(b.ref),
  );
  const recommendations = audits.reduce(
    (sum, audit) => sum + audit.recommendations.length,
    0,
  );
  return (
    <div className="space-y-10">
      <div className="max-w-2xl space-y-3">
        <p className="text-sm">
          <Link
            href="/en/jamforelse/"
            className="text-ink underline underline-offset-2"
          >
            {en.chain.backToTable}
          </Link>
        </p>
        <h1 className="text-4xl font-semibold tracking-tight">
          {underlag.country}
        </h1>
        <p className="text-ink-secondary">
          {count.format(audits.length)} {en.jamforelse.table.audits.toLowerCase()}
          {" · "}
          {count.format(recommendations)} {en.chain.recommendationsCount}
        </p>
      </div>
      <div className="space-y-12">
        {audits.map((audit) => (
          <ChainAudit
            key={audit.report_path}
            audit={audit}
            labels={en.chain}
          />
        ))}
      </div>
    </div>
  );
}

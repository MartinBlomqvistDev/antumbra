import type { Metadata } from "next";
import { PageIntro } from "@/components/shell";
import { en } from "@/content/en";

export const metadata: Metadata = { title: en.uppslag.title };

export default function LookUp() {
  return (
    <div className="space-y-6">
      <PageIntro
        title={en.uppslag.title}
        lead={en.uppslag.lead}
        building={en.building}
      />
      <p className="max-w-2xl rounded-lg border border-border-soft bg-surface-raised p-4 text-sm">
        {en.uppslag.banner}
      </p>
    </div>
  );
}

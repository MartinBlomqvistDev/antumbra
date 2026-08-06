import type { Metadata } from "next";
import { PageIntro } from "@/components/shell";
import { sv } from "@/content/sv";

export const metadata: Metadata = { title: sv.uppslag.title };

export default function Uppslag() {
  return (
    <div className="space-y-6">
      <PageIntro
        title={sv.uppslag.title}
        lead={sv.uppslag.lead}
        building={sv.building}
      />
      <p className="max-w-2xl rounded-lg border border-border-soft bg-surface-raised p-4 text-sm">
        {sv.uppslag.banner}
      </p>
    </div>
  );
}

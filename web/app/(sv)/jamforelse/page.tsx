import type { Metadata } from "next";
import { PageIntro } from "@/components/shell";
import { sv } from "@/content/sv";

export const metadata: Metadata = { title: sv.jamforelse.title };

export default function Jamforelse() {
  return (
    <PageIntro
      title={sv.jamforelse.title}
      lead={sv.jamforelse.lead}
      building={sv.building}
    />
  );
}

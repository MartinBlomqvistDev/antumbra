import type { Metadata } from "next";
import { PageIntro } from "@/components/shell";
import { en } from "@/content/en";

export const metadata: Metadata = { title: en.jamforelse.title };

export default function Comparison() {
  return (
    <PageIntro
      title={en.jamforelse.title}
      lead={en.jamforelse.lead}
      building={en.building}
    />
  );
}

import type { Metadata } from "next";
import { PageIntro } from "@/components/shell";
import { sv } from "@/content/sv";

export const metadata: Metadata = { title: sv.metod.title };

export default function Metod() {
  return (
    <PageIntro
      title={sv.metod.title}
      lead={sv.metod.lead}
      building={sv.building}
    />
  );
}

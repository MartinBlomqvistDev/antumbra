import type { Metadata } from "next";
import { PageIntro } from "@/components/shell";
import { en } from "@/content/en";

export const metadata: Metadata = { title: en.metod.title };

export default function Method() {
  return (
    <PageIntro
      title={en.metod.title}
      lead={en.metod.lead}
      building={en.building}
    />
  );
}

import type { Metadata } from "next";
import { PageIntro } from "@/components/shell";
import { sv } from "@/content/sv";

const copy = sv.data!;

export const metadata: Metadata = { title: copy.title };

export default function DataPage() {
  return (
    <PageIntro title={copy.title} lead={copy.lead} building={sv.building} />
  );
}

import type { Metadata } from "next";
import { PageIntro } from "@/components/shell";
import { sv } from "@/content/sv";

const copy = sv.handlingar!;

export const metadata: Metadata = { title: copy.title };

export default function Handlingar() {
  return (
    <PageIntro title={copy.title} lead={copy.lead} building={sv.building} />
  );
}

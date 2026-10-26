import type { Metadata } from "next";
import { About } from "@/components/about";
import { sv } from "@/content/sv";

const copy = sv.om!;

export const metadata: Metadata = { title: copy.title };

export default function Om() {
  return <About copy={copy} />;
}

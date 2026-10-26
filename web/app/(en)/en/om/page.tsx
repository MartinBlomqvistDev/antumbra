import type { Metadata } from "next";
import { About } from "@/components/about";
import { en } from "@/content/en";

const copy = en.om!;

export const metadata: Metadata = { title: copy.title };

export default function AboutEnglish() {
  return <About copy={copy} />;
}

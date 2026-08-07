import type { Metadata } from "next";
import { JamforelseView } from "@/components/jamforelse-view";
import { en } from "@/content/en";

export const metadata: Metadata = { title: en.jamforelse.title };

export default function Comparison() {
  return (
    <JamforelseView copy={en} locale="en-GB" hrefBase="/en/jamforelse/" />
  );
}

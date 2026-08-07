import type { Metadata } from "next";
import { JamforelseView } from "@/components/jamforelse-view";
import { sv } from "@/content/sv";

export const metadata: Metadata = { title: sv.jamforelse.title };

export default function Jamforelse() {
  return <JamforelseView copy={sv} locale="sv-SE" hrefBase="/jamforelse/" />;
}

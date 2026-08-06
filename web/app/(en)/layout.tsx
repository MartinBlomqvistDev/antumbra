import type { Metadata } from "next";
import type { ReactNode } from "react";
import { Shell } from "@/components/shell";
import { en } from "@/content/en";
import "../globals.css";

export const metadata: Metadata = {
  title: { default: en.site.name, template: `%s · ${en.site.name}` },
  description: en.site.description,
};

export default function EnLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body className="flex min-h-screen flex-col">
        <Shell copy={en}>{children}</Shell>
      </body>
    </html>
  );
}

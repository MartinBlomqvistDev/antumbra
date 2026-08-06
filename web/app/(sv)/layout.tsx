import type { Metadata } from "next";
import type { ReactNode } from "react";
import { Shell } from "@/components/shell";
import { sv } from "@/content/sv";
import "../globals.css";

export const metadata: Metadata = {
  title: { default: sv.site.name, template: `%s · ${sv.site.name}` },
  description: sv.site.description,
};

export default function SvLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="sv">
      <body className="flex min-h-screen flex-col">
        <Shell copy={sv}>{children}</Shell>
      </body>
    </html>
  );
}

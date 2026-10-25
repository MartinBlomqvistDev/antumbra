import type { Metadata } from "next";
import type { ReactNode } from "react";
import { Shell } from "@/components/shell";
import { sv } from "@/content/sv";
import "@fontsource-variable/source-serif-4";
import "@fontsource/ibm-plex-mono/400.css";
import "@fontsource/ibm-plex-mono/500.css";
import "../globals.css";

export const metadata: Metadata = {
  title: { default: sv.site.name, template: `%s · ${sv.site.name}` },
  description: sv.site.description,
};

export default function SvLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="sv">
      <head>
        <script
          dangerouslySetInnerHTML={{
            __html:
              'try{var t=localStorage.getItem("theme");' +
              "if(t)document.documentElement.dataset.theme=t}catch(e){}",
          }}
        />
      </head>
      <body className="flex min-h-screen flex-col">
        <Shell copy={sv}>{children}</Shell>
      </body>
    </html>
  );
}

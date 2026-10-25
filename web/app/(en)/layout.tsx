import type { Metadata } from "next";
import type { ReactNode } from "react";
import { Shell } from "@/components/shell";
import { en } from "@/content/en";
import "@fontsource-variable/source-serif-4";
import "@fontsource/ibm-plex-mono/400.css";
import "@fontsource/ibm-plex-mono/500.css";
import "../globals.css";

export const metadata: Metadata = {
  title: { default: en.site.name, template: `%s · ${en.site.name}` },
  description: en.site.description,
};

export default function EnLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
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
        <Shell copy={en}>{children}</Shell>
      </body>
    </html>
  );
}

import type { Metadata } from "next";
import type { ReactNode } from "react";
import { Shell } from "@/components/shell";
import { en } from "@/content/en";
import "@fontsource/spectral/400.css";
import "@fontsource/spectral/400-italic.css";
import "@fontsource/spectral/600.css";
import "@fontsource/fragment-mono/400.css";
import "../globals.css";

/** The card a shared link unfurls as; see the Swedish layout for the why. */
export const metadata: Metadata = {
  metadataBase: new URL("https://antumbraprojektet.se"),
  title: { default: en.site.name, template: `%s · ${en.site.name}` },
  description: en.site.description,
  openGraph: {
    type: "website",
    locale: "en_GB",
    url: "/en/",
    siteName: en.site.name,
    title: en.site.name,
    description: en.site.tagline,
    images: [
      { url: "/og.png", width: 1280, height: 640, alt: en.site.cardAlt },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: en.site.name,
    description: en.site.tagline,
    images: ["/og.png"],
  },
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

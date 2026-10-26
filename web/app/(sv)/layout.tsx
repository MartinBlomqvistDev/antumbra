import type { Metadata } from "next";
import type { ReactNode } from "react";
import { Shell } from "@/components/shell";
import { sv } from "@/content/sv";
import "@fontsource/spectral/400.css";
import "@fontsource/spectral/400-italic.css";
import "@fontsource/spectral/600.css";
import "@fontsource/fragment-mono/400.css";
import "../globals.css";

/**
 * The card a shared link unfurls as. Without it a link to the measurement is
 * a grey default box wherever it is posted, and the image is built from the
 * site's own tokens rather than from a stock photograph: it carries the two
 * figures and the question, so the card says what the page says.
 */
export const metadata: Metadata = {
  metadataBase: new URL("https://antumbraprojektet.se"),
  title: { default: sv.site.name, template: `%s · ${sv.site.name}` },
  description: sv.site.description,
  openGraph: {
    type: "website",
    locale: "sv_SE",
    url: "/",
    siteName: sv.site.name,
    title: sv.site.name,
    description: sv.site.tagline,
    images: [
      { url: "/og.png", width: 1280, height: 640, alt: sv.site.cardAlt },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: sv.site.name,
    description: sv.site.tagline,
    images: ["/og.png"],
  },
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

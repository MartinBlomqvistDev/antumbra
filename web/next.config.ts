import type { NextConfig } from "next";

/**
 * Static export. Every page is prerendered to HTML at build time and served as
 * plain files, with no runtime service behind them. The retrieval API that
 * /uppslag used to call was measured on 26 October 2026, came third of three,
 * and is deleted; the page now carries the six baked example answers and the
 * figures that removed the search box. No server, no runtime cost.
 */
const nextConfig: NextConfig = {
  output: "export",
  images: { unoptimized: true },
  trailingSlash: true,
};

export default nextConfig;

import type { NextConfig } from "next";

/**
 * Static export. Every page is prerendered to HTML at build time and served
 * as plain files; the only runtime service is the retrieval API, which the
 * /uppslag page calls from the browser. No server, no runtime cost.
 */
const nextConfig: NextConfig = {
  output: "export",
  images: { unoptimized: true },
  trailingSlash: true,
};

export default nextConfig;

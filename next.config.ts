import type { NextConfig } from "next";

// Security headers: no request leaves the origin except a learner clicking an
// external judge/CEMC link; the app has no API routes, no cookies, no server state to protect,
// so the CSP only needs to stop framing and plugin content, not script origins.
const securityHeaders = [
  { key: "X-Content-Type-Options", value: "nosniff" },
  { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
  {
    key: "Permissions-Policy",
    value: [
      "accelerometer=()",
      "camera=()",
      "geolocation=()",
      "gyroscope=()",
      "magnetometer=()",
      "microphone=()",
      "payment=()",
      "usb=()",
    ].join(", "),
  },
  {
    key: "Content-Security-Policy",
    value: "frame-ancestors 'none'; object-src 'none'",
  },
];

const nextConfig: NextConfig = {
  reactStrictMode: true,
  // Stop `next dev` from writing its agent-rules block into AGENTS.md.
  agentRules: false,
  // ETCCC_DIST_DIR: a plain `next build` writes to `.next`, which is also where `next dev`
  // writes — running one while the other is up kills the dev server (BUILD_ID changes under it).
  // Set it to build into a separate directory while `next dev` is running. Unset (the default)
  // resolves to `.next`, which Vercel's deployment build and `npm run dev`/`start` always use.
  distDir: process.env.ETCCC_DIST_DIR || ".next",
  // No `output: 'export'`: a regular Vercel build keeps next.config headers and redirects working.
  async redirects() {
    return [
      {
        // Each module used to hold its reading under a third segment (/learn/s1/M1.1/<slug>).
        // Every module is now one page, so an old link lands on it (308; the query passes through).
        source: "/learn/:stage/:module/:slug",
        destination: "/learn/:stage/:module",
        permanent: true,
      },
    ];
  },
  async headers() {
    return [
      {
        source: "/:path*",
        headers: securityHeaders,
      },
    ];
  },
};

export default nextConfig;

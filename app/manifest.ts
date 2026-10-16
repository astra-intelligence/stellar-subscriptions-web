import type { MetadataRoute } from "next";

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: "Stellar Subscriptions",
    short_name: "Stellar Subs",
    description:
      "Recurring payments on Stellar, on your terms. Authorize a spending cap once, cancel anytime.",
    start_url: "/",
    display: "standalone",
    background_color: "#090b10",
    theme_color: "#090b10",
    icons: [
      {
        src: "/icon.svg",
        sizes: "any",
        type: "image/svg+xml",
      },
    ],
  };
}

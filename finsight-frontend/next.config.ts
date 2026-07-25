import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Allow backend API URL to be configured via environment variable
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
  },
  // Suppress hydration warnings from Plotly's dynamic rendering
  reactStrictMode: false,
};

export default nextConfig;

import type { Metadata } from "next";
import "./globals.css";
import AmexNav from "@/components/layout/AmexNav";

export const metadata: Metadata = {
  title: "FinSight AI — Enterprise Customer Analytics",
  description:
    "Enterprise Customer Analytics & Decision Intelligence Platform for financial institutions.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <link
          href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap"
          rel="stylesheet"
        />
      </head>
      <body>
        <AmexNav />
        <div className="page-content">{children}</div>
      </body>
    </html>
  );
}

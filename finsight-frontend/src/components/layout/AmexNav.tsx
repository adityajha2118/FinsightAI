"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const NAV_ITEMS = [
  { href: "/dashboard", label: "Overview" },
  { href: "/customers", label: "Customer Intelligence" },
  { href: "/campaigns", label: "Campaign Analytics" },
  { href: "/compliance", label: "Compliance" },
  { href: "/complaints", label: "Complaint Intelligence" },
];

export default function AmexNav() {
  const pathname = usePathname();
  const isLanding = pathname === "/";

  return (
    <>
      {/* Centurion Stripe */}
      <div className="centurion-stripe" />

      {/* Navigation Bar */}
      <nav className="lp-nav">
        <div className="lp-nav-inner">
          {/* Logo */}
          <Link href="/" className="lp-nav-logo">
            <div className="lp-nav-logo-box">AMEX</div>
            <span className="lp-nav-logo-text">FinSight AI</span>
          </Link>

          {/* Nav Links */}
          <div className="lp-nav-links">
            {NAV_ITEMS.map(({ href, label }) => (
              <Link
                key={href}
                href={href}
                className={`lp-nav-link ${pathname === href ? "active" : ""} ${isLanding && href === "/dashboard" ? "active" : ""}`}
              >
                {label}
              </Link>
            ))}
          </div>

          {/* Right Side */}
          <div className="lp-nav-right">
            <span className="lp-nav-author">Built by Aditya Kumar Jha</span>
            <a
              href="https://github.com/adityajha2118/FinsightAI"
              target="_blank"
              rel="noopener noreferrer"
              className="lp-btn lp-btn-primary"
            >
              View on GitHub
            </a>
          </div>
        </div>
      </nav>
    </>
  );
}

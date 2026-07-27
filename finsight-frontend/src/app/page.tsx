"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import {
  Users, Megaphone, ShieldCheck, MessageSquareWarning,
  FlaskConical, LayoutDashboard
} from "lucide-react";
import { api } from "@/lib/api";

const MODULES = [
  {
    icon: Users,
    title: "Customer Intelligence",
    desc: "XGBoost-powered churn prediction, customer segmentation, and lifetime value analysis across 100,000+ cardmember profiles.",
    href: "/customers",
  },
  {
    icon: Megaphone,
    title: "Campaign Analytics",
    desc: "Multi-channel campaign performance tracking with ROI attribution, channel optimization, and real-time conversion metrics.",
    href: "/campaigns",
  },
  {
    icon: ShieldCheck,
    title: "Compliance Analytics",
    desc: "Automated regulatory compliance monitoring with risk scoring, anomaly detection, and audit-ready reporting dashboards.",
    href: "/compliance",
  },
  {
    icon: MessageSquareWarning,
    title: "Complaint Intelligence",
    desc: "NLP-driven complaint classification and sentiment analysis with AI-powered routing and resolution time optimization.",
    href: "/complaints",
  },
  {
    icon: FlaskConical,
    title: "Experimentation Hub",
    desc: "A/B testing framework with statistical significance calculations, variant analysis, and experiment lifecycle management.",
    href: "/experimentation",
  },
  {
    icon: LayoutDashboard,
    title: "Executive Dashboard",
    desc: "Unified command center with real-time KPIs, cross-module insights, and drill-down analytics for leadership decision-making.",
    href: "/dashboard",
  },
];

const TECH = [
  "Next.js", "React", "TypeScript", "Tailwind CSS",
  "FastAPI", "Python", "PostgreSQL", "SQLAlchemy",
  "XGBoost", "scikit-learn", "Plotly", "Render", "Vercel",
];

export default function LandingPage() {
  const [customerOverview, setCustomerOverview] = useState<any>(null);
  const [complaintKpis, setComplaintKpis] = useState<any>(null);

  useEffect(() => {
    api.customers.getOverview().then(setCustomerOverview).catch(() => {});
    api.complaints.getKpis().then(setComplaintKpis).catch(() => {});
  }, []);

  const totalCustomers = customerOverview?.total_customers;
  const churnRatePct = customerOverview?.churn_rate_pct;
  const totalComplaints = complaintKpis?.total_complaints;

  return (
    <div>

      {/* ── Hero Section ─────────────────────────────────── */}
      <section className="lp-hero" id="overview">
        <div className="lp-hero-inner">
          {/* Left column */}
          <div>
            <p className="lp-hero-eyebrow">Enterprise Fintech Analytics</p>
            <h1 className="lp-hero-headline">
              Customer Intelligence,<br />Reimagined.
            </h1>
            <p className="lp-hero-sub">
              FinSight AI simulates how American Express analyzes customer behavior
              — predicting churn, detecting compliance risk, routing complaints with AI,
              and surfacing intelligence for every level of the organization.
            </p>
            <div className="lp-hero-buttons">
              <Link href="/dashboard" className="lp-btn lp-btn-primary">
                Explore Dashboard
              </Link>
              <a
                href="https://github.com/adityajha2118/FinsightAI"
                target="_blank"
                rel="noopener noreferrer"
                className="lp-btn lp-btn-outline"
              >
                View Architecture
              </a>
            </div>
          </div>

          {/* Right column — Amex card */}
          <div>
            <div className="amex-card">
              <div className="amex-card-watermark">AMEX</div>
              <div className="amex-card-brand">American Express</div>
              <div className="amex-card-center">
                <div className="amex-card-centurion">
                  <div className="amex-card-centurion-inner">
                    <div className="amex-card-centurion-face" />
                  </div>
                </div>
              </div>
              <div className="amex-card-bottom">
                <div>
                  <p className="amex-card-label">Analytics Platform</p>
                  <p className="amex-card-title">FinSight AI Platform</p>
                </div>
                <div className="amex-card-chip">
                  <div className="amex-card-chip-left" />
                  <div className="amex-card-chip-right">
                    <div /><div />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ── KPI Strip ────────────────────────────────────── */}
      <div className="lp-kpi-strip">
        <div className="lp-kpi-strip-inner">
          <div className="lp-kpi-item">
            <div className="lp-kpi-val">
              {totalCustomers ? totalCustomers.toLocaleString() : "—"}
            </div>
            <div className="lp-kpi-lbl">Customers Analyzed</div>
          </div>
          <div className="lp-kpi-item">
            <div className="lp-kpi-val">
              {churnRatePct != null ? `${churnRatePct}%` : "—"}
            </div>
            <div className="lp-kpi-lbl">Churn Rate Detected</div>
          </div>
          <div className="lp-kpi-item">
            <div className="lp-kpi-val">
              {totalComplaints ? totalComplaints.toLocaleString() : "—"}
            </div>
            <div className="lp-kpi-lbl">Complaints Processed</div>
          </div>
          <div className="lp-kpi-item">
            <div className="lp-kpi-val">NLP-Powered</div>
            <div className="lp-kpi-lbl">Complaint Routing</div>
          </div>
        </div>
      </div>

      {/* ── Platform Modules ─────────────────────────────── */}
      <section className="lp-section" style={{ background: "#FFFFFF" }}>
        <div className="lp-section-inner">
          <p className="lp-section-label">Platform Modules</p>
          <h2 className="lp-section-title">Six Integrated Analytics Engines</h2>
          <p className="lp-section-sub">
            Each module connects to a shared PostgreSQL data layer, powering
            real-time dashboards with production-grade machine learning.
          </p>
          <div className="lp-cards-grid">
            {MODULES.map(({ icon: Icon, title, desc, href }) => (
              <div className="lp-card" key={title}>
                <div className="lp-card-icon">
                  <Icon />
                </div>
                <h3>{title}</h3>
                <p>{desc}</p>
                <Link href={href} className="lp-card-link">
                  Explore →
                </Link>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Section Stripe ───────────────────────────────── */}
      <div className="lp-section-stripe" />

      {/* ── Tech Stack ───────────────────────────────────── */}
      <div className="lp-tech-strip">
        <div className="lp-tech-inner">
          <p className="lp-tech-label">Built With</p>
          <div className="lp-tech-badges">
            {TECH.map((t) => (
              <span className="lp-tech-badge" key={t}>{t}</span>
            ))}
          </div>
        </div>
      </div>

      {/* ── Footer ───────────────────────────────────────── */}
      <footer className="lp-footer">
        <div className="lp-footer-inner">
          <div className="lp-footer-grid">
            {/* Column 1 — Brand */}
            <div>
              <div className="lp-footer-logo">
                <div className="lp-footer-logo-box">AMEX</div>
                <span className="lp-footer-logo-text">FinSight AI</span>
              </div>
              <p className="lp-footer-desc">
                An enterprise-grade analytics simulation inspired by
                American Express, built to demonstrate full-stack data
                engineering, machine learning, and modern frontend development.
              </p>
            </div>

            {/* Column 2 — Quick Links */}
            <div>
              <h4>Quick Links</h4>
              <div className="lp-footer-links">
                <Link href="/dashboard">Executive Dashboard</Link>
                <a href="https://github.com/adityajha2118/FinsightAI" target="_blank" rel="noopener noreferrer">GitHub Repository</a>
                <Link href="/customers">Customer Analytics</Link>
                <Link href="/complaints">Complaint Analytics</Link>
              </div>
            </div>

            {/* Column 3 — Modules */}
            <div>
              <h4>Analytics Modules</h4>
              <div className="lp-footer-links">
                <Link href="/customers">Customer Intelligence</Link>
                <Link href="/campaigns">Campaign Analytics</Link>
                <Link href="/compliance">Compliance</Link>
                <Link href="/experimentation">Experimentation</Link>
              </div>
            </div>

            {/* Column 4 — Connect */}
            <div>
              <h4>Connect</h4>
              <div className="lp-footer-author">
                Aditya Kumar Jha<br />
                Data Science &amp; Analytics<br />
              </div>
              <div className="lp-footer-social">
                <a href="https://github.com/adityajha2118" target="_blank" rel="noopener noreferrer" aria-label="GitHub">
                  <svg viewBox="0 0 24 24"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
                </a>
                <a href="https://linkedin.com/in/adityajha2118" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn">
                  <svg viewBox="0 0 24 24"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
                </a>
              </div>
            </div>
          </div>
        </div>
        <div className="lp-footer-bottom">
          <div className="lp-footer-bottom-inner">
            <p>© 2025 FinSight AI — Portfolio Project by Aditya Kumar Jha</p>
            <p>Not affiliated with American Express Company</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

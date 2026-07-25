"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard, Users, MessageSquareWarning, Megaphone,
  ShieldCheck, FlaskConical, Activity, BookOpen
} from "lucide-react";

const NAV_ITEMS = [
  { href: "/", label: "Executive Dashboard", icon: LayoutDashboard },
  { href: "/customers", label: "Customer Analytics", icon: Users },
  { href: "/complaints", label: "Complaint Analytics", icon: MessageSquareWarning },
  { href: "/campaigns", label: "Campaign Analytics", icon: Megaphone },
  { href: "/compliance", label: "Compliance Analytics", icon: ShieldCheck },
  { href: "/experimentation", label: "Experimentation", icon: FlaskConical },
  { href: "https://github.com/adityajha2118/FinsightAI/tree/main/notebooks", label: "Jupyter Notebooks", icon: BookOpen, external: true },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="sidebar">
      {/* Logo */}
      <div className="px-6 mb-6">
        <div className="flex items-center gap-2.5">
          <div className="w-9 h-9 rounded-lg flex items-center justify-center"
               style={{ background: "var(--gradient-primary)" }}>
            <Activity className="w-5 h-5 text-white" />
          </div>
          <div>
            <h1 className="text-base font-bold text-white tracking-tight">FinSight AI</h1>
            <p className="text-[10px] text-slate-500 font-medium tracking-wider uppercase">
              Enterprise Analytics
            </p>
          </div>
        </div>
      </div>

      {/* Divider */}
      <div className="mx-4 mb-3 border-t border-slate-700/50" />

      {/* Navigation */}
      <nav className="flex-1">
        <p className="px-6 mb-2 text-[10px] font-semibold text-slate-500 uppercase tracking-widest">
          Modules
        </p>
        {NAV_ITEMS.map(({ href, label, icon: Icon, external }) => {
          const isActive = pathname === href;
          if (external) {
            return (
              <a
                key={href}
                href={href}
                target="_blank"
                rel="noopener noreferrer"
                className="sidebar-link mt-4 opacity-80 hover:opacity-100"
              >
                <Icon className="w-4 h-4 flex-shrink-0" />
                <span>{label}</span>
              </a>
            );
          }
          return (
            <Link
              key={href}
              href={href}
              className={`sidebar-link ${isActive ? "active" : ""}`}
            >
              <Icon className="w-4 h-4 flex-shrink-0" />
              <span>{label}</span>
            </Link>
          );
        })}
      </nav>

      {/* Footer */}
      <div className="px-6 pt-4 border-t border-slate-700/50">
        <p className="text-[10px] text-slate-600">
          FinSight AI v2.0 &middot; PostgreSQL &middot; FastAPI &middot; Next.js
        </p>
      </div>
    </aside>
  );
}

"use client";

import dynamic from "next/dynamic";
import type { PlotParams } from "react-plotly.js";

const Plot = dynamic(() => import("react-plotly.js"), { ssr: false });

interface ChartCardProps {
  title: string;
  subtitle?: string;
  data: PlotParams["data"];
  layout?: Partial<PlotParams["layout"]>;
  height?: number;
  className?: string;
}

/** Reusable Plotly chart wrapper with dark theme defaults. */
export default function ChartCard({
  title,
  subtitle,
  data,
  layout = {},
  height = 340,
  className = "",
}: ChartCardProps) {
  const defaultLayout: Partial<PlotParams["layout"]> = {
    height,
    margin: { t: 30, r: 20, b: 50, l: 60 },
    paper_bgcolor: "transparent",
    plot_bgcolor: "transparent",
    font: { family: "Inter, system-ui", color: "#94a3b8", size: 12 },
    xaxis: {
      gridcolor: "rgba(148,163,184,0.08)",
      linecolor: "rgba(148,163,184,0.15)",
      zerolinecolor: "rgba(148,163,184,0.08)",
      ...((layout as any).xaxis || {}),
    },
    yaxis: {
      gridcolor: "rgba(148,163,184,0.08)",
      linecolor: "rgba(148,163,184,0.15)",
      zerolinecolor: "rgba(148,163,184,0.08)",
      ...((layout as any).yaxis || {}),
    },
    legend: { font: { color: "#94a3b8" }, ...(layout.legend || {}) },
    colorway: ["#6366f1", "#3b82f6", "#10b981", "#f59e0b", "#f43f5e", "#8b5cf6", "#06b6d4", "#ec4899"],
    ...layout,
  };

  return (
    <div className={`chart-container ${className}`}>
      <div className="mb-2">
        <h3 className="text-sm font-semibold text-slate-200">{title}</h3>
        {subtitle && <p className="text-xs text-slate-500 mt-0.5">{subtitle}</p>}
      </div>
      <Plot
        data={data}
        layout={defaultLayout}
        config={{ displayModeBar: false, responsive: true }}
        style={{ width: "100%" }}
      />
    </div>
  );
}

"use client";

import { useEffect, useState } from "react";
import KpiCard from "@/components/ui/KpiCard";
import ChartCard from "@/components/charts/ChartCard";
import { api } from "@/lib/api";
import { formatNumber, formatPct } from "@/lib/utils";

export default function ExperimentationPage() {
  const [results, setResults] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.experimentation.getResults().then(setResults).catch(console.error).finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="flex items-center justify-center h-96"><p className="text-slate-400">Loading experimentation results...</p></div>;
  if (!results || results.error) return <div className="text-rose-400">No experiment data found.</div>;

  const ctrl = results.group_metrics?.control;
  const treat = results.group_metrics?.treatment;
  const chi = results.chi_square_test;
  const tt = results.t_test_revenue;
  const ci = results.confidence_interval;
  const eff = results.effect_size;

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-white">Experimentation Analytics</h1>
        <p className="text-sm text-slate-400 mt-1">A/B test analysis with statistical rigor — T-Test, Chi-Square, confidence intervals, effect size</p>
        <div className="mt-3 flex flex-wrap gap-2 text-xs">
          <span className="text-slate-500">Source Datasets:</span>
          <a href="https://drive.google.com/drive/u/0/folders/1ykHLArsfczJXl5yDcc2nJncw0jGG4dD3" target="_blank" rel="noopener noreferrer" className="text-indigo-400 hover:text-indigo-300 hover:underline">bank_campaign.csv</a>
          <span className="text-slate-600">|</span>
          <a href="https://drive.google.com/drive/u/0/folders/1ykHLArsfczJXl5yDcc2nJncw0jGG4dD3" target="_blank" rel="noopener noreferrer" className="text-indigo-400 hover:text-indigo-300 hover:underline">customer_data.csv</a>
        </div>
      </div>

      {/* Experiment Header */}
      <div className="chart-container mb-6 flex items-center justify-between">
        <div>
          <h2 className="text-lg font-bold text-indigo-400">{results.experiment_name}</h2>
          <p className="text-sm text-slate-400">{formatNumber(results.total_participants)} participants</p>
        </div>
        <div className={`badge ${results.recommendation_status === "positive" ? "badge-success" : results.recommendation_status === "negative" ? "badge-danger" : "badge-warning"}`} style={{ fontSize: "0.8rem", padding: "0.4rem 1rem" }}>
          {results.recommendation_status === "positive" ? "✅ Significant Improvement" :
           results.recommendation_status === "negative" ? "❌ Significant Decline" : "⏳ Not Significant"}
        </div>
      </div>

      {/* KPIs */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-8">
        <KpiCard label="Lift" value={`${results.lift_pct > 0 ? "+" : ""}${results.lift_pct}%`} icon="📈" accentColor={results.lift_pct > 0 ? "#10b981" : "#f43f5e"} />
        <KpiCard label="P-Value (χ²)" value={chi?.p_value?.toFixed(4) || "N/A"} icon="📊" accentColor={chi?.significant ? "#10b981" : "#f59e0b"} />
        <KpiCard label="Effect Size" value={`${eff?.cohens_h?.toFixed(3)} (${eff?.cohens_h_interpretation})`} icon="📐" accentColor="#8b5cf6" />
        <KpiCard label="CI (95%)" value={`[${ci?.ci_lower?.toFixed(3)}, ${ci?.ci_upper?.toFixed(3)}]`} icon="📏" accentColor="#3b82f6" />
        <KpiCard label="Power" value={results.statistical_power ? formatPct(results.statistical_power * 100) : "N/A"} icon="⚡" accentColor="#6366f1" />
      </div>

      {/* Control vs Treatment Comparison */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <ChartCard
          title="Conversion Rate: Control vs Treatment"
          subtitle="Primary success metric comparison"
          data={[{
            x: ["Control", "Treatment"],
            y: [ctrl?.conversion_rate * 100, treat?.conversion_rate * 100],
            type: "bar" as const,
            marker: { color: ["#64748b", "#6366f1"] },
            text: [`${(ctrl?.conversion_rate * 100).toFixed(1)}%`, `${(treat?.conversion_rate * 100).toFixed(1)}%`],
            textposition: "auto" as const,
            textfont: { color: "#f1f5f9", size: 14, family: "Inter" },
          }]}
          layout={{ yaxis: { title: "Conversion Rate (%)" } }}
        />

        <ChartCard
          title="Average Revenue: Control vs Treatment"
          subtitle="Revenue per user comparison"
          data={[{
            x: ["Control", "Treatment"],
            y: [ctrl?.avg_revenue, treat?.avg_revenue],
            type: "bar" as const,
            marker: { color: ["#64748b", "#10b981"] },
            text: [`$${ctrl?.avg_revenue?.toFixed(2)}`, `$${treat?.avg_revenue?.toFixed(2)}`],
            textposition: "auto" as const,
            textfont: { color: "#f1f5f9", size: 14, family: "Inter" },
          }]}
          layout={{ yaxis: { title: "Avg Revenue ($)" } }}
        />
      </div>

      {/* Detailed Metrics Comparison */}
      <div className="chart-container mb-6">
        <h3 className="text-sm font-semibold text-slate-200 mb-3">Group Metrics Comparison</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left">
            <thead className="text-xs text-slate-400 uppercase border-b border-slate-700">
              <tr>
                <th className="py-2 px-4">Metric</th>
                <th className="py-2 px-4">Control</th>
                <th className="py-2 px-4">Treatment</th>
                <th className="py-2 px-4">Difference</th>
              </tr>
            </thead>
            <tbody>
              {[
                { name: "Sample Size", c: ctrl?.sample_size, t: treat?.sample_size },
                { name: "Conversions", c: ctrl?.conversions, t: treat?.conversions },
                { name: "Conversion Rate", c: `${(ctrl?.conversion_rate * 100).toFixed(2)}%`, t: `${(treat?.conversion_rate * 100).toFixed(2)}%`, d: `${results.lift_pct > 0 ? "+" : ""}${results.lift_pct}%` },
                { name: "Avg Revenue", c: `$${ctrl?.avg_revenue?.toFixed(2)}`, t: `$${treat?.avg_revenue?.toFixed(2)}`, d: `$${(treat?.avg_revenue - ctrl?.avg_revenue)?.toFixed(2)}` },
                { name: "Avg Sessions", c: ctrl?.avg_sessions?.toFixed(2), t: treat?.avg_sessions?.toFixed(2) },
                { name: "Avg Pages Viewed", c: ctrl?.avg_pages_viewed?.toFixed(2), t: treat?.avg_pages_viewed?.toFixed(2) },
                { name: "Avg Time Spent (min)", c: ctrl?.avg_time_spent?.toFixed(2), t: treat?.avg_time_spent?.toFixed(2) },
              ].map((row) => (
                <tr key={row.name} className="border-b border-slate-800">
                  <td className="py-2 px-4 font-medium">{row.name}</td>
                  <td className="py-2 px-4 text-slate-300">{row.c}</td>
                  <td className="py-2 px-4 text-indigo-400 font-medium">{row.t}</td>
                  <td className="py-2 px-4 text-emerald-400">{row.d || "—"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Statistical Tests */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
        <div className="chart-container">
          <h3 className="text-sm font-semibold text-slate-200 mb-2">Chi-Square Test</h3>
          <p className="text-xs text-slate-400 mb-3">Tests whether conversion proportions differ significantly</p>
          <div className="space-y-2 text-sm">
            <p>χ² Statistic: <span className="text-indigo-400 font-mono">{chi?.statistic?.toFixed(4)}</span></p>
            <p>P-Value: <span className={`font-mono font-bold ${chi?.significant ? "text-emerald-400" : "text-amber-400"}`}>{chi?.p_value?.toFixed(6)}</span></p>
            <p>Significant: <span className={chi?.significant ? "text-emerald-400" : "text-amber-400"}>{chi?.significant ? "Yes ✅" : "No ⏳"}</span></p>
          </div>
        </div>

        <div className="chart-container">
          <h3 className="text-sm font-semibold text-slate-200 mb-2">Welch&apos;s T-Test (Revenue)</h3>
          <p className="text-xs text-slate-400 mb-3">Tests whether mean revenue differs significantly</p>
          <div className="space-y-2 text-sm">
            <p>T Statistic: <span className="text-indigo-400 font-mono">{tt?.statistic?.toFixed(4)}</span></p>
            <p>P-Value: <span className={`font-mono font-bold ${tt?.significant ? "text-emerald-400" : "text-amber-400"}`}>{tt?.p_value?.toFixed(6)}</span></p>
            <p>Significant: <span className={tt?.significant ? "text-emerald-400" : "text-amber-400"}>{tt?.significant ? "Yes ✅" : "No ⏳"}</span></p>
          </div>
        </div>

        <div className="chart-container">
          <h3 className="text-sm font-semibold text-slate-200 mb-2">Effect Size</h3>
          <p className="text-xs text-slate-400 mb-3">Practical significance of the observed difference</p>
          <div className="space-y-2 text-sm">
            <p>Cohen&apos;s h: <span className="text-indigo-400 font-mono">{eff?.cohens_h?.toFixed(4)}</span> ({eff?.cohens_h_interpretation})</p>
            <p>Cohen&apos;s d (Revenue): <span className="text-indigo-400 font-mono">{eff?.cohens_d_revenue?.toFixed(4)}</span> ({eff?.cohens_d_interpretation})</p>
            <p>95% CI: <span className="text-blue-400 font-mono">[{ci?.ci_lower?.toFixed(4)}, {ci?.ci_upper?.toFixed(4)}]</span></p>
          </div>
        </div>
      </div>

      {/* Recommendation */}
      <div className={`recommendation-box ${results.recommendation_status === "positive" ? "" : results.recommendation_status === "negative" ? "border-rose-500/30" : "border-amber-500/30"}`}
           style={results.recommendation_status === "positive" ? {} : results.recommendation_status === "negative" ? { background: "linear-gradient(135deg, rgba(244,63,94,0.08), rgba(225,29,72,0.08))" } : { background: "linear-gradient(135deg, rgba(245,158,11,0.08), rgba(217,119,6,0.08))" }}>
        <h3>📊 Statistical Recommendation</h3>
        <p className="mt-2">{results.recommendation}</p>
      </div>
    </div>
  );
}

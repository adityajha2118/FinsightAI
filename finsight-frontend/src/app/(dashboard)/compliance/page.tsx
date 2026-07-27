"use client";

import { useEffect, useState } from "react";
import KpiCard from "@/components/ui/KpiCard";
import ChartCard from "@/components/charts/ChartCard";
import { api } from "@/lib/api";
import { formatNumber, formatPct } from "@/lib/utils";

export default function ComplianceAnalyticsPage() {
  const [kpis, setKpis] = useState<any>(null);
  const [riskDist, setRiskDist] = useState<any[]>([]);
  const [highRisk, setHighRisk] = useState<any[]>([]);
  const [countryRisk, setCountryRisk] = useState<any[]>([]);
  const [sectorRisk, setSectorRisk] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      api.compliance.getKpis().then(setKpis),
      api.compliance.getRiskDistribution().then(setRiskDist),
      api.compliance.getHighRisk(50).then(setHighRisk),
      api.compliance.getCountryRisk().then(setCountryRisk),
      api.compliance.getSectorRisk().then(setSectorRisk),
    ]).catch(console.error).finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="flex items-center justify-center h-96"><p className="text-amex-gray-600">Loading compliance analytics...</p></div>;

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-amex-gray-900">Compliance Analytics</h1>
        <p className="text-sm text-amex-gray-600 mt-1">AML/KYC risk assessment, PEP monitoring, and sanctions screening</p>
        <div className="mt-3 flex flex-wrap gap-2 text-xs">
          <span className="text-amex-gray-600">Source Datasets:</span>
          <a href="https://drive.google.com/drive/u/0/folders/1ykHLArsfczJXl5yDcc2nJncw0jGG4dD3" target="_blank" rel="noopener noreferrer" className="text-amex-blue hover:text-amex-blue-dark hover:underline">kyc_part1.csv</a>
          <span className="text-amex-gray-300">|</span>
          <a href="https://drive.google.com/drive/u/0/folders/1ykHLArsfczJXl5yDcc2nJncw0jGG4dD3" target="_blank" rel="noopener noreferrer" className="text-amex-blue hover:text-amex-blue-dark hover:underline">kyc_part2.csv</a>
        </div>
        <div className="mt-1 flex flex-wrap gap-2 text-xs">
          <span className="text-amex-gray-600">Related Notebooks:</span>
          <a href="https://github.com/adityajha2118/FinsightAI/tree/main/notebooks/01_data_understanding/04_kyc_eda.ipynb" target="_blank" rel="noopener noreferrer" className="text-amex-blue hover:text-amex-blue-dark hover:underline">04_kyc_eda.ipynb</a>
          <span className="text-amex-gray-300">|</span>
          <a href="https://github.com/adityajha2118/FinsightAI/tree/main/notebooks/01_data_understanding/10_kyc_risk_prediction.ipynb" target="_blank" rel="noopener noreferrer" className="text-amex-blue hover:text-amex-blue-dark hover:underline">10_kyc_risk_prediction.ipynb</a>
        </div>
      </div>

      {/* KPIs */}
      {kpis && (
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-8">
          <KpiCard label="Total Profiles" value={formatNumber(kpis.total_profiles)} icon="🛡️" accentColor="#006FCF" />
          <KpiCard label="High Risk" value={formatNumber(kpis.high_risk_count)} icon="🚨" accentColor="#C0001A" />
          <KpiCard label="PEP Flagged" value={formatNumber(kpis.pep_count)} icon="👔" accentColor="#C07000" />
          <KpiCard label="Sanctions Match" value={formatNumber(kpis.sanctions_count)} icon="⛔" accentColor="#e11d48" />
          <KpiCard label="Risk Rate" value={formatPct(kpis.compliance_risk_pct)} icon="📊" accentColor="#004A8F" />
        </div>
      )}

      {/* Row 1: Risk Distribution + Country */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        {riskDist.length > 0 && (
          <ChartCard
            title="Risk Tier Distribution"
            subtitle="Customer distribution across compliance risk tiers"
            data={[{
              labels: riskDist.map(d => d.risk_tier),
              values: riskDist.map(d => d.profile_count),
              type: "pie" as const, hole: 0.5,
              textinfo: "label+percent",
              textfont: { color: "#ffffff", size: 11 },
              marker: {
                colors: riskDist.map(d =>
                  d.risk_tier === "Critical" ? "#e11d48" :
                  d.risk_tier === "High" ? "#C0001A" :
                  d.risk_tier === "Medium" ? "#C07000" : "#008000"
                ),
              },
            }]}
          />
        )}
        {countryRisk.length > 0 && (
          <ChartCard
            title="Country Risk Analysis"
            subtitle="Entity distribution by country with PEP and sanctions flags"
            data={[
              {
                x: countryRisk.slice(0, 12).map(d => d.country),
                y: countryRisk.slice(0, 12).map(d => d.profile_count),
                type: "bar" as const, name: "Profiles",
                marker: { color: "#006FCF" },
              },
              {
                x: countryRisk.slice(0, 12).map(d => d.country),
                y: countryRisk.slice(0, 12).map(d => d.pep_count),
                type: "bar" as const, name: "PEP",
                marker: { color: "#C07000" },
              },
              {
                x: countryRisk.slice(0, 12).map(d => d.country),
                y: countryRisk.slice(0, 12).map(d => d.sanctions_count),
                type: "bar" as const, name: "Sanctions",
                marker: { color: "#C0001A" },
              },
            ]}
            layout={{ barmode: "group" as const, xaxis: { tickangle: -45 } }}
            height={380}
          />
        )}
      </div>

      {/* Sector Risk */}
      {sectorRisk.length > 0 && (
        <ChartCard
          title="Sector Risk Distribution"
          subtitle="Risk levels across industry sectors"
          className="mb-6"
          data={[{
            x: sectorRisk.map(d => d.sector),
            y: sectorRisk.map(d => d.profile_count),
            type: "bar" as const,
            marker: {
              color: sectorRisk.map(d =>
                d.sector_risk === "High" ? "#C0001A" :
                d.sector_risk === "Medium" ? "#C07000" : "#008000"
              ),
            },
            text: sectorRisk.map(d => d.sector_risk),
            textposition: "auto" as const,
            textfont: { color: "#ffffff", size: 9 },
          }]}
          layout={{ xaxis: { tickangle: -45 } }}
          height={320}
        />
      )}

      {/* High Risk Table */}
      {highRisk.length > 0 && (
        <div className="chart-container mb-6">
          <h3 className="text-sm font-semibold text-slate-200 mb-3">🚨 High Risk Entities — Requires Enhanced Due Diligence</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-sm text-left">
              <thead className="text-xs text-amex-gray-600 uppercase border-b border-slate-700">
                <tr>
                  <th className="py-2 px-3">Client ID</th>
                  <th className="py-2 px-3">Name</th>
                  <th className="py-2 px-3">Sector</th>
                  <th className="py-2 px-3">Country</th>
                  <th className="py-2 px-3">PEP</th>
                  <th className="py-2 px-3">Sanctions</th>
                  <th className="py-2 px-3">Opacity</th>
                  <th className="py-2 px-3">Flags</th>
                </tr>
              </thead>
              <tbody>
                {highRisk.slice(0, 20).map((r: any) => (
                  <tr key={r.profile_id} className="border-b border-slate-800 hover:bg-slate-800/30">
                    <td className="py-2 px-3 font-mono text-xs">{r.client_id}</td>
                    <td className="py-2 px-3">{r.client_name}</td>
                    <td className="py-2 px-3">{r.sector}</td>
                    <td className="py-2 px-3">{r.country}</td>
                    <td className="py-2 px-3">{r.pep_flag ? <span className="badge badge-warning">PEP</span> : "—"}</td>
                    <td className="py-2 px-3">{r.sanctions_flag ? <span className="badge badge-danger">YES</span> : "—"}</td>
                    <td className="py-2 px-3">{(r.ownership_opacity_score || 0).toFixed(2)}</td>
                    <td className="py-2 px-3 font-bold text-amex-red">{r.total_flags}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Recommendations */}
      <div className="recommendation-box">
        <h3>💡 Business Recommendations</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mt-3">
          <p>• <strong>Critical</strong> tier entities require immediate review — freeze accounts and initiate compliance investigation.</p>
          <p>• PEP-flagged entities need periodic 30-day enhanced due diligence reviews regardless of other risk factors.</p>
          <p>• High-opacity entities (score &gt; 0.7) should undergo beneficial ownership verification to ensure regulatory compliance.</p>
          <p>• Countries with high sanctions counts should be added to enhanced monitoring lists with transaction limits.</p>
        </div>
      </div>
    </div>
  );
}

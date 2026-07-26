"use client";

import { useEffect, useState } from "react";
import KpiCard from "@/components/ui/KpiCard";
import ChartCard from "@/components/charts/ChartCard";
import { api } from "@/lib/api";
import { formatNumber, formatPct, formatCategory } from "@/lib/utils";

export default function CampaignAnalyticsPage() {
  const [kpis, setKpis] = useState<any>(null);
  const [byJob, setByJob] = useState<any[]>([]);
  const [byEdu, setByEdu] = useState<any[]>([]);
  const [byContact, setByContact] = useState<any[]>([]);
  const [fatigue, setFatigue] = useState<any[]>([]);
  const [monthly, setMonthly] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      api.campaigns.getKpis().then(setKpis),
      api.campaigns.getByJob().then(setByJob),
      api.campaigns.getByEducation().then(setByEdu),
      api.campaigns.getByContact().then(setByContact),
      api.campaigns.getFatigue().then(setFatigue),
      api.campaigns.getMonthly().then(setMonthly),
    ]).catch(console.error).finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="flex items-center justify-center h-96"><p className="text-slate-400">Loading campaign analytics...</p></div>;

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-white">Campaign Analytics</h1>
        <p className="text-sm text-slate-400 mt-1">Analyze conversion rates, demographic performance, and communication channels</p>
        <div className="mt-3 flex flex-wrap gap-2 text-xs">
          <span className="text-slate-500">Source Datasets:</span>
          <a href="https://drive.google.com/drive/u/0/folders/1ykHLArsfczJXl5yDcc2nJncw0jGG4dD3" target="_blank" rel="noopener noreferrer" className="text-indigo-400 hover:text-indigo-300 hover:underline">bank_campaign.csv</a>
        </div>
        <div className="mt-1 flex flex-wrap gap-2 text-xs">
          <span className="text-slate-500">Related Notebooks:</span>
          <a href="https://github.com/adityajha2118/FinsightAI/tree/main/notebooks/01_data_understanding/03_campaign_eda.ipynb" target="_blank" rel="noopener noreferrer" className="text-indigo-400 hover:text-indigo-300 hover:underline">03_campaign_eda.ipynb</a>
          <span className="text-slate-600">|</span>
          <a href="https://github.com/adityajha2118/FinsightAI/tree/main/notebooks/01_data_understanding/09_campaign_prediction.ipynb" target="_blank" rel="noopener noreferrer" className="text-indigo-400 hover:text-indigo-300 hover:underline">09_campaign_prediction.ipynb</a>
        </div>
      </div>

      {/* KPIs */}
      {kpis && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          <KpiCard label="Total Contacts" value={formatNumber(kpis.total_contacts)} icon="📞" accentColor="#6366f1" />
          <KpiCard label="Conversions" value={formatNumber(kpis.conversions)} icon="✅" accentColor="#10b981" />
          <KpiCard label="Success Rate" value={formatPct(kpis.success_rate_pct)} icon="🎯" accentColor="#8b5cf6" />
          <KpiCard label="Non-Conversions" value={formatNumber((kpis.total_contacts || 0) - (kpis.conversions || 0))} icon="❌" accentColor="#f43f5e" />
        </div>
      )}

      {/* Row 1: Monthly Trend + By Contact */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        {monthly.length > 0 && (
          <ChartCard
            title="Conversion Rate by Month"
            subtitle="Seasonal patterns in campaign effectiveness"
            data={[{
              x: monthly.map(d => d.month),
              y: monthly.map(d => d.conversion_rate),
              type: "bar" as const,
              marker: { color: "#6366f1" },
              text: monthly.map(d => `${d.conversion_rate}%`),
              textposition: "auto" as const,
              textfont: { color: "#f1f5f9", size: 10 },
            }]}
            layout={{ yaxis: { title: "Conversion Rate (%)" } }}
          />
        )}
        {byContact.length > 0 && (
          <ChartCard
            title="Conversion by Contact Method"
            subtitle="Cellular vs telephone effectiveness"
            data={[{
              x: byContact.map(d => d.contact),
              y: byContact.map(d => d.conversion_rate),
              type: "bar" as const,
              marker: { color: ["#10b981", "#3b82f6"] },
              text: byContact.map(d => `${d.conversion_rate}% (${d.conversions}/${d.total})`),
              textposition: "auto" as const,
              textfont: { color: "#f1f5f9", size: 10 },
            }]}
            layout={{ yaxis: { title: "Conversion Rate (%)" } }}
          />
        )}
      </div>

      {/* Row 2: By Job + By Education */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        {byJob.length > 0 && (
          <ChartCard
            title="Conversion Rate by Job"
            subtitle="Which job types convert best"
            data={[{
              y: byJob.map(d => formatCategory(d.job)),
              x: byJob.map(d => d.conversion_rate),
              type: "bar" as const, orientation: "h" as const,
              marker: { color: "#8b5cf6" },
            }]}
            layout={{ yaxis: { automargin: true }, margin: { l: 120 } }}
            height={380}
          />
        )}
        {byEdu.length > 0 && (
          <ChartCard
            title="Conversion Rate by Education"
            subtitle="Education level and campaign receptiveness"
            data={[{
              y: byEdu.map(d => formatCategory(d.education)),
              x: byEdu.map(d => d.conversion_rate),
              type: "bar" as const, orientation: "h" as const,
              marker: { color: "#3b82f6" },
            }]}
            layout={{ yaxis: { automargin: true }, margin: { l: 140 } }}
            height={380}
          />
        )}
      </div>

      {/* Campaign Fatigue */}
      {fatigue.length > 0 && (
        <ChartCard
          title="Campaign Fatigue Analysis"
          subtitle="Conversion rate drops as number of contacts increases — identifies optimal contact frequency"
          className="mb-6"
          data={[
            {
              x: fatigue.map(d => d.contacts_made),
              y: fatigue.map(d => d.conversion_rate),
              type: "scatter" as const, mode: "lines+markers" as const,
              name: "Conversion Rate",
              line: { color: "#6366f1", width: 2.5 },
              marker: { size: 6 },
              yaxis: "y",
            },
            {
              x: fatigue.map(d => d.contacts_made),
              y: fatigue.map(d => d.total_customers),
              type: "bar" as const,
              name: "Customers",
              marker: { color: "rgba(99,102,241,0.15)" },
              yaxis: "y2",
            },
          ]}
          layout={{
            xaxis: { title: "Number of Contacts" },
            yaxis: { title: "Conversion Rate (%)", side: "left" },
            yaxis2: { title: "Customer Count", side: "right", overlaying: "y" },
            legend: { x: 0.5, y: 1.15, orientation: "h" as const },
          }}
          height={350}
        />
      )}

      {/* Recommendations */}
      <div className="recommendation-box">
        <h3>💡 Business Recommendations</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mt-3">
          <p>• <strong>Cellular</strong> outperforms telephone — shift budget to cellular channels for higher conversion ROI.</p>
          <p>• Conversion drops significantly after 3-4 contacts — cap campaigns to prevent customer fatigue and negative brand perception.</p>
          <p>• Target job types with the highest conversion rates — concentrate outreach on receptive segments.</p>
          <p>• Seasonal analysis shows specific months perform better — align major campaigns with peak conversion periods.</p>
        </div>
      </div>
    </div>
  );
}

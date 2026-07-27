"use client";

import { useEffect, useState } from "react";
import KpiCard from "@/components/ui/KpiCard";
import ChartCard from "@/components/charts/ChartCard";
import { api } from "@/lib/api";
import { formatNumber, formatPct, formatCurrency, formatCategory } from "@/lib/utils";

export default function ExecutiveDashboard() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.dashboard.getSummary().then(setData).catch(console.error).finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-amex-gray-600 text-lg">Loading executive dashboard...</div>
      </div>
    );
  }

  if (!data) {
    return <div className="text-amex-red">Failed to load dashboard data. Is the backend running?</div>;
  }

  const kpis = [
    { label: "Total Customers", value: formatNumber(data.total_customers), icon: "👥", accent: "#006FCF" },
    { label: "Total Complaints", value: formatNumber(data.total_complaints), icon: "📋", accent: "#C07000" },
    { label: "Complaint Growth", value: formatPct(data.complaint_growth_pct), icon: "📈", accent: data.complaint_growth_pct > 0 ? "#C0001A" : "#008000", dir: data.complaint_growth_pct > 0 ? "up" as const : "down" as const },
    { label: "Avg Resolution Time", value: `${data.avg_resolution_days?.toFixed(1) || 0}d`, icon: "⏱️", accent: "#006FCF" },
    { label: "Timely Response", value: formatPct(data.timely_response_pct), icon: "✅", accent: "#008000" },
    { label: "Customer Churn", value: formatPct(data.churn_rate_pct), icon: "⚠️", accent: "#C0001A" },
    { label: "Campaign Success", value: formatPct(data.campaign_success_pct), icon: "🎯", accent: "#004A8F" },
    { label: "Compliance Risk", value: formatPct(data.compliance_risk_pct), icon: "🛡️", accent: "#C07000" },
    { label: "Negative Sentiment", value: formatPct(data.negative_sentiment_pct), icon: "😤", accent: "#C0001A" },
    { label: "High Risk Entities", value: formatNumber(data.high_risk_count), icon: "🚨", accent: "#e11d48" },
  ];

  return (
    <div>
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-amex-gray-900">Executive Dashboard</h1>
        <p className="text-sm text-amex-gray-600 mt-1">
          C-level overview across all analytics domains — powered by PostgreSQL
        </p>
        <div className="mt-3 flex flex-wrap gap-2 text-xs">
          <span className="text-amex-gray-600">Source Datasets:</span>
          <a href="https://drive.google.com/drive/u/0/folders/1ykHLArsfczJXl5yDcc2nJncw0jGG4dD3" target="_blank" rel="noopener noreferrer" className="text-amex-blue hover:text-amex-blue-dark hover:underline">customer_data.csv</a>
          <span className="text-amex-gray-300">|</span>
          <a href="https://drive.google.com/drive/u/0/folders/1ykHLArsfczJXl5yDcc2nJncw0jGG4dD3" target="_blank" rel="noopener noreferrer" className="text-amex-blue hover:text-amex-blue-dark hover:underline">transactions.csv</a>
          <span className="text-amex-gray-300">|</span>
          <a href="https://drive.google.com/drive/u/0/folders/1ykHLArsfczJXl5yDcc2nJncw0jGG4dD3" target="_blank" rel="noopener noreferrer" className="text-amex-blue hover:text-amex-blue-dark hover:underline">bank_transactions.csv</a>
          <span className="text-amex-gray-300">|</span>
          <a href="https://drive.google.com/drive/u/0/folders/1ykHLArsfczJXl5yDcc2nJncw0jGG4dD3" target="_blank" rel="noopener noreferrer" className="text-amex-blue hover:text-amex-blue-dark hover:underline">cfpb_complaints.csv</a>
          <span className="text-amex-gray-300">|</span>
          <a href="https://drive.google.com/drive/u/0/folders/1ykHLArsfczJXl5yDcc2nJncw0jGG4dD3" target="_blank" rel="noopener noreferrer" className="text-amex-blue hover:text-amex-blue-dark hover:underline">bank_campaign.csv</a>
          <span className="text-amex-gray-300">|</span>
          <a href="https://drive.google.com/drive/u/0/folders/1ykHLArsfczJXl5yDcc2nJncw0jGG4dD3" target="_blank" rel="noopener noreferrer" className="text-amex-blue hover:text-amex-blue-dark hover:underline">kyc_part1.csv</a>
          <span className="text-amex-gray-300">|</span>
          <a href="https://drive.google.com/drive/u/0/folders/1ykHLArsfczJXl5yDcc2nJncw0jGG4dD3" target="_blank" rel="noopener noreferrer" className="text-amex-blue hover:text-amex-blue-dark hover:underline">kyc_part2.csv</a>
        </div>
        <div className="mt-1 flex flex-wrap gap-2 text-xs">
          <span className="text-amex-gray-600">Related Notebooks:</span>
          <a href="https://github.com/adityajha2118/FinsightAI/tree/main/notebooks/01_data_understanding/13_unified_customer_profile.ipynb" target="_blank" rel="noopener noreferrer" className="text-amex-blue hover:text-amex-blue-dark hover:underline">13_unified_customer_profile.ipynb</a>
        </div>
      </div>

      {/* KPI Grid */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4 mb-8">
        {kpis.map((k) => (
          <KpiCard key={k.label} label={k.label} value={k.value} icon={k.icon} accentColor={k.accent} />
        ))}
      </div>

      {/* Charts Row 1 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        {/* Monthly Complaint Trend */}
        {data.monthly_complaints?.length > 0 && (
          <ChartCard
            title="Monthly Complaint Trend"
            subtitle="Volume of complaints received over time"
            data={[{
              x: data.monthly_complaints.map((d: any) => d.month),
              y: data.monthly_complaints.map((d: any) => d.complaint_count),
              type: "scatter" as const,
              mode: "lines+markers" as const,
              fill: "tozeroy",
              fillcolor: "rgba(99,102,241,0.1)",
              line: { color: "#006FCF", width: 2.5 },
              marker: { size: 4 },
            }]}
            layout={{ xaxis: { title: "Month" }, yaxis: { title: "Complaints" } }}
          />
        )}

        {/* Complaints by Product */}
        {data.complaints_by_product?.length > 0 && (
          <ChartCard
            title="Complaints by Product"
            subtitle="Which products drive the most complaints"
            data={[{
              x: data.complaints_by_product.map((d: any) => d.complaint_count).reverse(),
              y: data.complaints_by_product.map((d: any) => formatCategory(d.product)).reverse(),
              type: "bar" as const,
              orientation: "h" as const,
              marker: {
                color: "#004A8F",
                borderRadius: 4,
              },
            }]}
            layout={{ 
              xaxis: { title: "Complaints" },
              margin: { l: 150 },
            }}
          />
        )}
      </div>

      {/* Charts Row 2 */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
        {/* Customer Health */}
        {data.customer_health_distribution?.length > 0 && (
          <ChartCard
            title="Customer Health Distribution"
            subtitle="Risk labels from churn prediction model"
            data={[{
              x: data.customer_health_distribution.map((d: any) => d.risk_label),
              y: data.customer_health_distribution.map((d: any) => d.customer_count),
              type: "bar" as const,
              marker: {
                color: data.customer_health_distribution.map((d: any) =>
                  d.risk_label === "High Risk" ? "#C0001A" :
                  d.risk_label === "Medium Risk" ? "#C07000" : "#008000"
                ),
                borderRadius: 6,
              },
            }]}
          />
        )}

        {/* Sentiment Distribution */}
        {data.sentiment_distribution?.length > 0 && (
          <ChartCard
            title="Sentiment Distribution"
            subtitle="VADER sentiment analysis of complaints"
            data={[{
              labels: data.sentiment_distribution.map((d: any) => d.sentiment_label),
              values: data.sentiment_distribution.map((d: any) => d.complaint_count),
              type: "pie" as const,
              hole: 0.5,
              textfont: { color: "#ffffff", size: 11 },
              marker: {
                colors: data.sentiment_distribution.map((d: any) =>
                  d.sentiment_label === "Negative" ? "#C0001A" :
                  d.sentiment_label === "Positive" ? "#008000" : "#64748b"
                ),
              },
            }]}
          />
        )}

        {/* Risk Distribution */}
        {data.risk_distribution?.length > 0 && (
          <ChartCard
            title="Compliance Risk Distribution"
            subtitle="KYC risk tier breakdown"
            data={[{
              x: data.risk_distribution.map((d: any) => d.risk_tier),
              y: data.risk_distribution.map((d: any) => d.profile_count),
              type: "bar" as const,
              marker: {
                color: data.risk_distribution.map((d: any) =>
                  d.risk_tier === "Critical" ? "#e11d48" :
                  d.risk_tier === "High" ? "#C0001A" :
                  d.risk_tier === "Medium" ? "#C07000" : "#008000"
                ),
              },
            }]}
          />
        )}
      </div>

      {/* Segment Distribution */}
      {data.segment_distribution?.length > 0 && (
        <div className="mb-6">
          <ChartCard
            title="Customer Segmentation"
            subtitle="K-Means cluster distribution across 5 behavioral segments"
            data={[{
              x: data.segment_distribution.map((d: any) => d.segment_name),
              y: data.segment_distribution.map((d: any) => d.customer_count),
              type: "bar" as const,
              marker: {
                color: ["#006FCF", "#006FCF", "#008000", "#C07000", "#004A8F"],
              },
            }]}
            height={300}
          />
        </div>
      )}

      {/* Business Insights */}
      <div className="recommendation-box">
        <h3>📊 Top Insights</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mt-3">
          <p>• Customer churn rate is <strong>{formatPct(data.churn_rate_pct)}</strong> — target customers with churn probability &gt; 0.7 for retention offers.</p>
          <p>• <strong>{formatPct(data.timely_response_pct)}</strong> of complaints receive timely responses — monitor products with low response rates.</p>
          <p>• Campaign success rate is <strong>{formatPct(data.campaign_success_pct)}</strong> — focus on high-converting segments to optimize ROI.</p>
          <p>• <strong>{formatNumber(data.high_risk_count)}</strong> entities flagged as high/critical risk — ensure enhanced due diligence reviews are current.</p>
        </div>
      </div>
    </div>
  );
}

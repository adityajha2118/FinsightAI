"use client";

import { useEffect, useState } from "react";
import KpiCard from "@/components/ui/KpiCard";
import ChartCard from "@/components/charts/ChartCard";
import { api } from "@/lib/api";
import { formatNumber, formatPct, formatCategory } from "@/lib/utils";

export default function ComplaintAnalyticsPage() {
  const [kpis, setKpis] = useState<any>(null);
  const [trends, setTrends] = useState<any[]>([]);
  const [byProduct, setByProduct] = useState<any[]>([]);
  const [byIssue, setByIssue] = useState<any[]>([]);
  const [byState, setByState] = useState<any[]>([]);
  const [sentiment, setSentiment] = useState<any[]>([]);
  const [sentimentByProduct, setSentimentByProduct] = useState<any[]>([]);
  const [responses, setResponses] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      api.complaints.getKpis().then(setKpis),
      api.complaints.getTrends().then(setTrends),
      api.complaints.getByProduct().then(setByProduct),
      api.complaints.getByIssue().then(setByIssue),
      api.complaints.getByState().then(setByState),
      api.complaints.getSentiment().then(setSentiment),
      api.complaints.getSentimentByProduct().then(setSentimentByProduct),
      api.complaints.getResponses().then(setResponses),
    ]).catch(console.error).finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="flex items-center justify-center h-96"><p className="text-slate-400">Loading complaint analytics...</p></div>;

  const products = Array.from(new Set(sentimentByProduct.map(d => d.product))).slice(0, 8);
  const formattedProducts = products.map(formatCategory);
  const posData = products.map(p => {
    const row = sentimentByProduct.find(d => d.product === p && d.sentiment_label === 'Positive');
    return row ? row.count : 0;
  });
  const negData = products.map(p => {
    const row = sentimentByProduct.find(d => d.product === p && d.sentiment_label === 'Negative');
    return row ? row.count : 0;
  });

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-white">Complaint Analytics</h1>
        <p className="text-sm text-slate-400 mt-1">Identify product issues, sentiment trends, and response efficiency</p>
        <div className="mt-3 flex flex-wrap gap-2 text-xs">
          <span className="text-slate-500">Source Datasets:</span>
          <a href="https://drive.google.com/drive/u/0/folders/1ykHLArsfczJXl5yDcc2nJncw0jGG4dD3" target="_blank" rel="noopener noreferrer" className="text-indigo-400 hover:text-indigo-300 hover:underline">cfpb_complaints.csv</a>
        </div>
        <div className="mt-1 flex flex-wrap gap-2 text-xs">
          <span className="text-slate-500">Related Notebooks:</span>
          <a href="https://github.com/adityajha2118/FinsightAI/tree/main/notebooks/01_data_understanding/05_complaint_eda.ipynb" target="_blank" rel="noopener noreferrer" className="text-indigo-400 hover:text-indigo-300 hover:underline">05_complaint_eda.ipynb</a>
          <span className="text-slate-600">|</span>
          <a href="https://github.com/adityajha2118/FinsightAI/tree/main/notebooks/01_data_understanding/11_complaint_sentiment.ipynb" target="_blank" rel="noopener noreferrer" className="text-indigo-400 hover:text-indigo-300 hover:underline">11_complaint_sentiment.ipynb</a>
          <span className="text-slate-600">|</span>
          <a href="https://github.com/adityajha2118/FinsightAI/tree/main/notebooks/01_data_understanding/12_escalation_prediction.ipynb" target="_blank" rel="noopener noreferrer" className="text-indigo-400 hover:text-indigo-300 hover:underline">12_escalation_prediction.ipynb</a>
        </div>
      </div>

      {/* KPIs */}
      {kpis && (
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-8">
          <KpiCard label="Total Complaints" value={formatNumber(kpis.total_complaints)} icon="📋" accentColor="#6366f1" />
          <KpiCard label="Complaint Growth" value={formatPct(kpis.complaint_growth_pct)} icon="📈" accentColor={kpis.complaint_growth_pct > 0 ? "#f43f5e" : "#10b981"} />
          <KpiCard label="Avg Resolution" value={`${(kpis.avg_resolution_days || 0).toFixed(1)}d`} icon="⏱️" accentColor="#3b82f6" />
          <KpiCard label="Timely Response" value={formatPct(kpis.timely_response_pct)} icon="✅" accentColor="#10b981" />
          <KpiCard label="Negative Sentiment" value={formatPct(kpis.negative_sentiment_pct)} icon="😤" accentColor="#f43f5e" />
        </div>
      )}

      {/* Row 1: Trend + Sentiment */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        {trends.length > 0 && (
          <ChartCard
            title="Monthly Complaint Trend"
            subtitle="Complaint volume over time"
            data={[{
              x: trends.map(d => d.month),
              y: trends.map(d => d.complaint_count),
              type: "scatter" as const, mode: "lines+markers" as const,
              fill: "tozeroy", fillcolor: "rgba(99,102,241,0.1)",
              line: { color: "#6366f1", width: 2 }, marker: { size: 4 },
            }]}
          />
        )}
        {sentiment.length > 0 && (
          <ChartCard
            title="VADER Sentiment Distribution"
            subtitle="Compound score classification across all complaints"
            data={[{
              labels: sentiment.map(d => d.sentiment_label),
              values: sentiment.map(d => d.complaint_count),
              type: "pie" as const, hole: 0.5,
              textinfo: "label+percent",
              textfont: { color: "#f1f5f9", size: 11 },
              marker: {
                colors: sentiment.map(d =>
                  d.sentiment_label === "Negative" ? "#f43f5e" :
                  d.sentiment_label === "Positive" ? "#10b981" : "#64748b"
                ),
              },
            }]}
          />
        )}
      </div>

      {/* Row 2: Product + Issue */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        {byProduct.length > 0 && (
          <ChartCard
            title="Complaints by Product"
            subtitle="Which products generate the most complaints"
            data={[{
              y: byProduct.slice(0, 10).map(d => formatCategory(d.product)),
              x: byProduct.slice(0, 10).map(d => d.complaint_count),
              type: "bar" as const, orientation: "h" as const,
              marker: { color: "#6366f1" },
            }]}
            layout={{ yaxis: { automargin: true }, margin: { l: 180 } }}
            height={380}
          />
        )}
        {byIssue.length > 0 && (
          <ChartCard
            title="Top Complaint Issues"
            subtitle="Most frequently reported issues"
            data={[{
              y: byIssue.slice(0, 10).map(d => d.issue),
              x: byIssue.slice(0, 10).map(d => d.complaint_count),
              type: "bar" as const, orientation: "h" as const,
              marker: { color: "#3b82f6" },
            }]}
            layout={{ yaxis: { automargin: true }, margin: { l: 200 } }}
            height={380}
          />
        )}
      </div>

      {/* New Row: Sentiment by Product + Company Response */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        {products.length > 0 && (
          <ChartCard
            title="Sentiment by Product"
            subtitle="Positive vs Negative sentiment breakdown across top products"
            data={[
              { x: formattedProducts, y: posData, name: 'Positive', type: "bar" as const, marker: { color: "#10b981" } },
              { x: formattedProducts, y: negData, name: 'Negative', type: "bar" as const, marker: { color: "#f43f5e" } }
            ]}
            layout={{ xaxis: { tickangle: -25, tickfont: { size: 10 } }, barmode: 'stack' }}
            height={380}
          />
        )}
        {responses.length > 0 && (
          <ChartCard
            title="Company Response Distribution"
            subtitle="How complaints were resolved"
            data={[{
              y: responses.slice(0, 10).map(d => d.company_response),
              x: responses.slice(0, 10).map(d => d.response_count),
              type: "bar" as const, orientation: "h" as const,
              marker: { color: "#f59e0b" },
            }]}
            layout={{ yaxis: { automargin: true }, margin: { l: 180 } }}
            height={380}
          />
        )}
      </div>

      {/* Business Recommendations */}
      <div className="recommendation-box">
        <h3>💡 Business Recommendations</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mt-3">
          <p>• Products with highest complaint volume need root cause analysis — check for systemic billing or servicing issues.</p>
          <p>• High negative sentiment complaints should be fast-tracked to priority support to prevent CFPB escalation.</p>
          <p>• States with disproportionate complaint counts may indicate regional service gaps or regulatory focus areas.</p>
          <p>• Monitor word frequency trends monthly to detect emerging issues before they become systemic problems.</p>
        </div>
      </div>
    </div>
  );
}

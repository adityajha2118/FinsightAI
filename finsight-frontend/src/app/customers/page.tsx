"use client";

import { useEffect, useState } from "react";
import KpiCard from "@/components/ui/KpiCard";
import ChartCard from "@/components/charts/ChartCard";
import { api } from "@/lib/api";
import { formatNumber, formatPct, formatCurrency, formatCategory } from "@/lib/utils";

export default function CustomerAnalyticsPage() {
  const [overview, setOverview] = useState<any>(null);
  const [segments, setSegments] = useState<any[]>([]);
  const [segProfiles, setSegProfiles] = useState<any[]>([]);
  const [churnDist, setChurnDist] = useState<any[]>([]);
  const [topChurn, setTopChurn] = useState<any[]>([]);
  const [inactive, setInactive] = useState<any[]>([]);
  const [transactions, setTransactions] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      api.customers.getOverview().then(setOverview),
      api.customers.getSegments().then(setSegments),
      api.customers.getSegmentProfiles().then(setSegProfiles),
      api.customers.getChurnDistribution().then(setChurnDist),
      api.customers.getTopChurn(30).then(setTopChurn),
      api.customers.getInactive(50).then(setInactive),
      api.customers.getTransactions().then(setTransactions),
    ]).catch(console.error).finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <div className="flex items-center justify-center h-96"><p className="text-slate-400">Loading customer analytics...</p></div>;
  }

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-white">Customer Analytics</h1>
        <p className="text-sm text-slate-400 mt-1">Segmentation, churn prediction, health scoring, and inactivity detection</p>
        <div className="mt-3 flex flex-wrap gap-2 text-xs">
          <span className="text-slate-500">Source Datasets:</span>
          <a href="https://drive.google.com/drive/u/0/folders/1ykHLArsfczJXl5yDcc2nJncw0jGG4dD3" target="_blank" rel="noopener noreferrer" className="text-indigo-400 hover:text-indigo-300 hover:underline">customer_data.csv</a>
          <span className="text-slate-600">|</span>
          <a href="https://drive.google.com/drive/u/0/folders/1ykHLArsfczJXl5yDcc2nJncw0jGG4dD3" target="_blank" rel="noopener noreferrer" className="text-indigo-400 hover:text-indigo-300 hover:underline">transactions.csv</a>
          <span className="text-slate-600">|</span>
          <a href="https://drive.google.com/drive/u/0/folders/1ykHLArsfczJXl5yDcc2nJncw0jGG4dD3" target="_blank" rel="noopener noreferrer" className="text-indigo-400 hover:text-indigo-300 hover:underline">bank_transactions.csv</a>
        </div>
        </div>
        <div className="mt-1 flex flex-wrap gap-2 text-xs">
          <span className="text-slate-500">Related Notebooks:</span>
          <a href="https://github.com/adityajha2118/FinsightAI/tree/main/notebooks/01_data_understanding/01_customer_eda.ipynb" target="_blank" rel="noopener noreferrer" className="text-indigo-400 hover:text-indigo-300 hover:underline">01_customer_eda.ipynb</a>
          <span className="text-slate-600">|</span>
          <a href="https://github.com/adityajha2118/FinsightAI/tree/main/notebooks/01_data_understanding/02_transaction_eda.ipynb" target="_blank" rel="noopener noreferrer" className="text-indigo-400 hover:text-indigo-300 hover:underline">02_transaction_eda.ipynb</a>
          <span className="text-slate-600">|</span>
          <a href="https://github.com/adityajha2118/FinsightAI/tree/main/notebooks/01_data_understanding/06_customer_segmentation.ipynb" target="_blank" rel="noopener noreferrer" className="text-indigo-400 hover:text-indigo-300 hover:underline">06_customer_segmentation.ipynb</a>
          <span className="text-slate-600">|</span>
          <a href="https://github.com/adityajha2118/FinsightAI/tree/main/notebooks/01_data_understanding/07_inactivity_detection.ipynb" target="_blank" rel="noopener noreferrer" className="text-indigo-400 hover:text-indigo-300 hover:underline">07_inactivity_detection.ipynb</a>
          <span className="text-slate-600">|</span>
          <a href="https://github.com/adityajha2118/FinsightAI/tree/main/notebooks/01_data_understanding/08_churn_prediction.ipynb" target="_blank" rel="noopener noreferrer" className="text-indigo-400 hover:text-indigo-300 hover:underline">08_churn_prediction.ipynb</a>
        </div>
      </div>

      {/* KPIs */}
      {overview && (
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-8">
          <KpiCard label="Total Customers" value={formatNumber(overview.total_customers)} icon="👥" accentColor="#6366f1" />
          <KpiCard label="Churn Rate" value={formatPct(overview.churn_rate_pct)} icon="⚠️" accentColor="#f43f5e" />
          <KpiCard label="Avg Credit Limit" value={formatCurrency(overview.avg_credit_limit)} icon="💳" accentColor="#3b82f6" />
          <KpiCard label="Avg Utilization" value={formatPct((overview.avg_utilization || 0) * 100)} icon="📊" accentColor="#10b981" />
          <KpiCard label="Churned Customers" value={formatNumber(overview.churned_customers)} icon="🚪" accentColor="#f59e0b" />
        </div>
      )}

      {/* Charts Row 1: Segmentation + Churn */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        {segments.length > 0 && (
          <ChartCard
            title="Customer Segmentation"
            subtitle="K-Means clustering (k=5) by spending behavior"
            data={[{
              labels: segments.map(d => d.segment_name),
              values: segments.map(d => d.customer_count),
              type: "pie" as const,
              hole: 0.45,
              textinfo: "label+percent",
              textfont: { color: "#f1f5f9", size: 10 },
              marker: { colors: ["#6366f1", "#3b82f6", "#10b981", "#f59e0b", "#8b5cf6"] },
            }]}
          />
        )}
        {churnDist.length > 0 && (
          <ChartCard
            title="Churn Risk Distribution"
            subtitle="XGBoost churn probability tier breakdown"
            data={[{
              x: churnDist.map(d => d.risk_label),
              y: churnDist.map(d => d.customer_count),
              type: "bar" as const,
              marker: {
                color: churnDist.map(d =>
                  d.risk_label === "High Risk" ? "#f43f5e" :
                  d.risk_label === "Medium Risk" ? "#f59e0b" : "#10b981"
                ),
              },
            }]}
          />
        )}
      </div>

      {/* Segment Profiles Table */}
      {segProfiles.length > 0 && (
        <div className="chart-container mb-6">
          <h3 className="text-sm font-semibold text-slate-200 mb-3">Segment Profiles — Average Metrics</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-sm text-left">
              <thead className="text-xs text-slate-400 uppercase border-b border-slate-700">
                <tr>
                  <th className="py-2 px-3">Segment</th>
                  <th className="py-2 px-3">Count</th>
                  <th className="py-2 px-3">Avg Credit Limit</th>
                  <th className="py-2 px-3">Avg Trans Amt</th>
                  <th className="py-2 px-3">Avg Trans Ct</th>
                  <th className="py-2 px-3">Avg Utilization</th>
                  <th className="py-2 px-3">Avg Churn Prob</th>
                </tr>
              </thead>
              <tbody>
                {segProfiles.map((s: any) => (
                  <tr key={s.segment_name} className="border-b border-slate-800 hover:bg-slate-800/30">
                    <td className="py-2 px-3 font-medium text-indigo-400">{s.segment_name}</td>
                    <td className="py-2 px-3">{formatNumber(s.customer_count)}</td>
                    <td className="py-2 px-3">{formatCurrency(s.avg_credit_limit)}</td>
                    <td className="py-2 px-3">{formatCurrency(s.avg_trans_amt)}</td>
                    <td className="py-2 px-3">{s.avg_trans_ct?.toFixed(0)}</td>
                    <td className="py-2 px-3">{formatPct((s.avg_utilization || 0) * 100)}</td>
                    <td className="py-2 px-3">{(s.avg_churn_prob || 0).toFixed(3)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Transaction Analysis */}
      {transactions.length > 0 && (
        <ChartCard
          title="Transaction Analysis by Category"
          subtitle="Spending distribution across merchant categories"
          className="mb-6"
          data={[{
            x: transactions.map(d => formatCategory(d.category)),
            y: transactions.map(d => d.total_amount),
            type: "bar" as const,
            marker: { color: "#6366f1" },
          }]}
          layout={{ xaxis: { tickangle: -45 }, yaxis: { title: "Total Amount ($)" } }}
          height={320}
        />
      )}

      {/* Top Churn Risk Table */}
      {topChurn.length > 0 && (
        <div className="chart-container mb-6">
          <h3 className="text-sm font-semibold text-slate-200 mb-3">🚨 High Churn Risk Customers</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-sm text-left">
              <thead className="text-xs text-slate-400 uppercase border-b border-slate-700">
                <tr>
                  <th className="py-2 px-3">Client ID</th>
                  <th className="py-2 px-3">Churn Prob</th>
                  <th className="py-2 px-3">Risk</th>
                  <th className="py-2 px-3">Segment</th>
                  <th className="py-2 px-3">Income</th>
                  <th className="py-2 px-3">Inactive Months</th>
                </tr>
              </thead>
              <tbody>
                {topChurn.slice(0, 15).map((c: any) => (
                  <tr key={c.client_id} className="border-b border-slate-800 hover:bg-slate-800/30">
                    <td className="py-2 px-3 font-mono text-xs">{c.client_id}</td>
                    <td className="py-2 px-3 font-semibold text-rose-400">{(c.churn_probability || 0).toFixed(3)}</td>
                    <td className="py-2 px-3">
                      <span className={`badge ${c.risk_label === "High Risk" ? "badge-danger" : c.risk_label === "Medium Risk" ? "badge-warning" : "badge-success"}`}>
                        {c.risk_label}
                      </span>
                    </td>
                    <td className="py-2 px-3 text-indigo-400">{c.segment_name}</td>
                    <td className="py-2 px-3">{c.income_category}</td>
                    <td className="py-2 px-3">{c.months_inactive_12_mon}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Business Recommendations */}
      <div className="recommendation-box">
        <h3>💡 Business Recommendations</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mt-3">
          <p>• Focus retention efforts on <strong>High Risk</strong> customers — offer fee waivers, reward boosts, or personalized outreach.</p>
          <p>• <strong>At-Risk Dormant</strong> segment shows high inactivity — trigger re-engagement campaigns with targeted promotions.</p>
          <p>• <strong>Premium Customers</strong> generate the most revenue — invest in loyalty programs to prevent churn in this segment.</p>
          <p>• Monitor customers with 3+ months of inactivity — silent attrition precedes formal churn by 60-90 days.</p>
        </div>
      </div>
    </div>
  );
}

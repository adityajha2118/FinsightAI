/**
 * FinSight AI — Backend API Client.
 *
 * Single module for all backend HTTP calls.
 * Every page fetches data through these functions.
 */

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

async function fetchApi<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    cache: "no-store",
  });
  if (!res.ok) {
    throw new Error(`API error ${res.status}: ${path}`);
  }
  return res.json();
}

// ── Dashboard ────────────────────────────────────────────────
export const api = {
  dashboard: {
    getSummary: () => fetchApi<any>("/api/dashboard/summary"),
  },

  customers: {
    getOverview: () => fetchApi<any>("/api/customers/overview"),
    getSegments: () => fetchApi<any[]>("/api/customers/segments"),
    getSegmentProfiles: () => fetchApi<any[]>("/api/customers/segment-profiles"),
    getChurnDistribution: () => fetchApi<any[]>("/api/customers/churn/distribution"),
    getTopChurn: (limit = 50) => fetchApi<any[]>(`/api/customers/churn/top?limit=${limit}`),
    getInactive: (limit = 100) => fetchApi<any[]>(`/api/customers/inactive?limit=${limit}`),
    getHealth: () => fetchApi<any[]>("/api/customers/health"),
    getTransactions: () => fetchApi<any[]>("/api/customers/transactions"),
  },

  complaints: {
    getKpis: () => fetchApi<any>("/api/complaints/kpis"),
    getTrends: () => fetchApi<any[]>("/api/complaints/trends"),
    getByProduct: () => fetchApi<any[]>("/api/complaints/by-product"),
    getByIssue: () => fetchApi<any[]>("/api/complaints/by-issue"),
    getByState: () => fetchApi<any[]>("/api/complaints/by-state"),
    getSentiment: () => fetchApi<any[]>("/api/complaints/sentiment"),
    getSentimentByProduct: () => fetchApi<any[]>("/api/complaints/sentiment-by-product"),
    getResponses: () => fetchApi<any[]>("/api/complaints/responses"),
    getWordcloud: (limit = 50) => fetchApi<any[]>(`/api/complaints/wordcloud?limit=${limit}`),
  },

  campaigns: {
    getKpis: () => fetchApi<any>("/api/campaigns/kpis"),
    getByJob: () => fetchApi<any[]>("/api/campaigns/by-job"),
    getByEducation: () => fetchApi<any[]>("/api/campaigns/by-education"),
    getByContact: () => fetchApi<any[]>("/api/campaigns/by-contact"),
    getFatigue: () => fetchApi<any[]>("/api/campaigns/fatigue"),
    getMonthly: () => fetchApi<any[]>("/api/campaigns/monthly"),
  },

  compliance: {
    getKpis: () => fetchApi<any>("/api/compliance/kpis"),
    getRiskDistribution: () => fetchApi<any[]>("/api/compliance/risk-distribution"),
    getHighRisk: (limit = 50) => fetchApi<any[]>(`/api/compliance/high-risk?limit=${limit}`),
    getCountryRisk: () => fetchApi<any[]>("/api/compliance/country-risk"),
    getSectorRisk: () => fetchApi<any[]>("/api/compliance/sector-risk"),
  },

  experimentation: {
    getExperiments: () => fetchApi<any[]>("/api/experimentation/experiments"),
    getResults: (name?: string) =>
      fetchApi<any>(name ? `/api/experimentation/results?experiment_name=${name}` : "/api/experimentation/results"),
  },

  predict: {
    churn: (data: any) =>
      fetch(`${API_BASE}/api/predict/churn`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      }).then((r) => r.json()),
    campaign: (data: any) =>
      fetch(`${API_BASE}/api/predict/campaign`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      }).then((r) => r.json()),
    compliance: (data: any) =>
      fetch(`${API_BASE}/api/predict/compliance`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      }).then((r) => r.json()),
  },

  health: () => fetchApi<any>("/api/health"),
};

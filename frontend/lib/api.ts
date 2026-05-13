import type {
  CampaignRecommendation,
  CampaignSimulationResult,
  ClusterPoint,
  CustomersResponse,
  DashboardSummary,
  Insight,
  ModelMetrics,
  RevenuePoint,
  SegmentSummary,
} from "./types";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
    cache: "no-store",
  });

  if (!res.ok) {
    throw new Error(`API request failed: ${res.status} ${res.statusText}`);
  }

  return res.json() as Promise<T>;
}

export const api = {
  summary: () => request<DashboardSummary>("/dashboard/summary"),
  revenue: () => request<RevenuePoint[]>("/dashboard/revenue"),
  segments: () => request<SegmentSummary[]>("/segments"),
  customers: (pageSize = 20) => request<CustomersResponse>(`/customers?page_size=${pageSize}&sort_by=Monetary&sort_desc=true`),
  recommendations: () => request<CampaignRecommendation[]>("/campaigns/recommendations"),
  insights: () => request<Insight[]>("/insights"),
  metrics: () => request<ModelMetrics>("/model/metrics"),
  clusterPoints: () => request<{ data: ClusterPoint[]; total: number; limit: number }>("/model/cluster-points?limit=600"),
  simulateCampaign: (body: {
    segment: string;
    campaign_type: string;
    budget: number;
    discount_pct: number;
    expected_conversion_rate: number;
  }) =>
    request<CampaignSimulationResult>("/campaigns/simulate", {
      method: "POST",
      body: JSON.stringify(body),
    }),
};

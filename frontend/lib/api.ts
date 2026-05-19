import type {
  CampaignRecommendation,
  CampaignSimulationResult,
  ClusterPoint,
  CustomersResponse,
  DataStatus,
  DataUploadResult,
  DatasetRegistry,
  DashboardSummary,
  Insight,
  ModelMetrics,
  RevenuePoint,
  SegmentSummary,
  PipelineConfig,
  SchemaInference,
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

async function uploadRequest<T>(path: string, body: FormData): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, {
    method: "POST",
    body,
    cache: "no-store",
  });

  if (!res.ok) {
    const errorText = await res.text();
    throw new Error(`API request failed: ${res.status} ${errorText}`);
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
  dataStatus: () => request<DataStatus>("/data/status"),
  datasets: () => request<DatasetRegistry>("/data/datasets"),
  setDatasetActive: (id: string, active: boolean) =>
    request<DataUploadResult>(`/data/datasets/${id}/activate`, {
      method: "POST",
      body: JSON.stringify({ active }),
    }),
  deleteDataset: (id: string) =>
    request<DataUploadResult>(`/data/datasets/${id}`, {
      method: "DELETE",
    }),
  config: () => request<PipelineConfig>("/data/config"),
  saveConfig: (body: Partial<PipelineConfig>) =>
    request<PipelineConfig>("/data/config", {
      method: "POST",
      body: JSON.stringify(body),
    }),
  retrainData: (config?: Partial<PipelineConfig>) =>
    request<DataUploadResult>("/data/retrain", {
      method: "POST",
      body: config ? JSON.stringify(config) : JSON.stringify({}),
    }),
  inferSchema: (file: File) => {
    const form = new FormData();
    form.append("file", file);
    return uploadRequest<SchemaInference>("/data/infer-schema", form);
  },
  uploadDataset: (file: File, retrain = true, mapping?: Record<string, string>, config?: Partial<PipelineConfig>) => {
    const form = new FormData();
    form.append("file", file);
    form.append("retrain", String(retrain));
    if (mapping) form.append("mapping", JSON.stringify(mapping));
    if (config) form.append("config", JSON.stringify(config));
    return uploadRequest<DataUploadResult>("/data/upload", form);
  },
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

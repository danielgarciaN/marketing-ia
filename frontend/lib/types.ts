export type DashboardSummary = {
  total_customers: number;
  total_revenue: number;
  total_orders: number;
  avg_order_value: number;
  avg_frequency: number;
  active_customers: number;
  inactive_customers: number;
  top_country: string;
  date_range?: { start: string; end: string };
};

export type RevenuePoint = {
  month: string;
  revenue: number;
};

export type SegmentSummary = {
  segment: string;
  count: number;
  total_revenue: number;
  avg_monetary: number;
  avg_frequency: number;
  avg_recency: number;
  avg_order_value: number;
  pct_revenue: number;
  pct_customers: number;
  description?: string;
  business_goal?: string;
};

export type Customer = {
  CustomerID: number;
  Country: string;
  Recency: number;
  Frequency: number;
  Monetary: number;
  AvgOrderValue: number;
  RFM_Score: number;
  Segment: string;
  Cluster: number;
};

export type CustomersResponse = {
  data: Customer[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
};

export type CampaignRecommendation = {
  segment: string;
  description: string;
  business_goal: string;
  campaigns: Array<{
    type: string;
    objective: string;
    message: string;
    priority: string;
  }>;
};

export type Insight = {
  id: string;
  category: string;
  title: string;
  insight: string;
  priority: string;
  action: string;
  impact: string;
};

export type ModelMetrics = {
  n_clusters: number;
  silhouette_score: number;
  inertia: number;
  eval_k: number[];
  eval_silhouette: number[];
  eval_inertia: number[];
};

export type ClusterPoint = {
  CustomerID: number;
  Segment: string;
  Cluster: number;
  PCA_1: number;
  PCA_2: number;
  Monetary: number;
  Frequency: number;
  Recency: number;
};

export type CampaignSimulationResult = {
  segment: string;
  campaign_type: string;
  budget: number;
  discount_pct: number;
  customers_in_segment: number;
  customers_reached: number;
  adjusted_conversion_rate: number;
  expected_conversions: number;
  estimated_revenue: number;
  campaign_cost: number;
  roi_pct: number;
  uplift_conversions: number;
  avg_order_value: number;
  recommendation: string;
  error?: string;
};

export type DataStatus = {
  raw_dataset: {
    exists: boolean;
    path?: string;
    bytes?: number;
    modified_at?: number;
  };
  processed_customers: {
    exists: boolean;
    path?: string;
    bytes?: number;
    modified_at?: number;
  };
  required_columns: string[];
  loaded_in_memory: boolean;
  customer_count?: number;
  segments?: string[];
};

export type DataUploadResult = {
  status: string;
  filename?: string;
  bytes?: number;
  raw_path?: string;
  retrained?: boolean;
  training?: {
    n_clusters: number;
    silhouette_score: number;
    inertia: number;
  };
};

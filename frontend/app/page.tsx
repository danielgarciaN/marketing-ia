"use client";

import { useEffect, useMemo, useState } from "react";
import {
  BarChart3,
  Brain,
  Database,
  LineChart,
  type LucideIcon,
  Loader2,
  Megaphone,
  Network,
  Table2,
  Users,
} from "lucide-react";
import { Bar, BarChart, CartesianGrid, Cell, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { api } from "@/lib/api";
import type {
  CampaignRecommendation,
  ClusterPoint,
  CustomersResponse,
  DashboardSummary,
  Insight,
  ModelMetrics,
  RevenuePoint,
  SegmentSummary,
} from "@/lib/types";
import { formatCurrency, formatNumber, segmentClass, type Currency } from "@/lib/format";
import {
  businessGoal,
  campaignLabel,
  campaignMessage,
  campaignObjective,
  copy,
  locales,
  segmentDescription,
  type Locale,
  segmentLabel,
} from "@/lib/i18n";
import { DashboardCard } from "@/components/DashboardCard";
import { RevenueChart } from "@/components/RevenueChart";
import { SegmentCard } from "@/components/SegmentCard";
import { CustomerTable } from "@/components/CustomerTable";
import { ClusterScatterPlot } from "@/components/ClusterScatterPlot";
import { CampaignSimulator } from "@/components/CampaignSimulator";
import { InsightCard } from "@/components/InsightCard";
import { DataManager } from "@/components/DataManager";

type View = "overview" | "data" | "customers" | "segments" | "clustering" | "campaigns" | "insights" | "methodology";

type AppData = {
  summary: DashboardSummary;
  revenue: RevenuePoint[];
  segments: SegmentSummary[];
  customers: CustomersResponse;
  recommendations: CampaignRecommendation[];
  insights: Insight[];
  metrics: ModelMetrics;
  clusterPoints: ClusterPoint[];
};

const navItems: Array<{ id: View; icon: LucideIcon }> = [
  { id: "overview", icon: BarChart3 },
  { id: "data", icon: Database },
  { id: "customers", icon: Users },
  { id: "segments", icon: Network },
  { id: "clustering", icon: LineChart },
  { id: "campaigns", icon: Megaphone },
  { id: "insights", icon: Brain },
  { id: "methodology", icon: Table2 },
];

const segmentColors = ["#2B5D7E", "#10B981", "#F59E0B", "#EF4444", "#22D3EE", "#7C3AED", "#5F6B73"];

export default function Home() {
  const [activeView, setActiveView] = useState<View>("overview");
  const [data, setData] = useState<AppData | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [selectedSegment, setSelectedSegment] = useState<string | null>(null);
  const [locale, setLocale] = useState<Locale>("en");
  const [currency, setCurrency] = useState<Currency>("GBP");
  const t = copy[locale];

  const loadData = async () => {
    try {
      setError(null);
      const [summary, revenue, segments, customers, recommendations, insights, metrics, clusterPoints] = await Promise.all([
        api.summary(),
        api.revenue(),
        api.segments(),
        api.customers(20),
        api.recommendations(),
        api.insights(),
        api.metrics(),
        api.clusterPoints(),
      ]);

      setData({
        summary,
        revenue,
        segments,
        customers,
        recommendations,
        insights,
        metrics,
        clusterPoints: clusterPoints.data,
      });
      setSelectedSegment((current) => current ?? segments[0]?.segment ?? null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not load API data");
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const selectedSegmentData = useMemo(() => {
    if (!data || !selectedSegment) return null;
    return data.segments.find((segment) => segment.segment === selectedSegment) ?? null;
  }, [data, selectedSegment]);

  const selectedRecommendation = useMemo(() => {
    if (!data || !selectedSegment) return null;
    return data.recommendations.find((item) => item.segment === selectedSegment) ?? null;
  }, [data, selectedSegment]);

  return (
    <main className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">AI</div>
          <div>
            <strong>Marketing Intel</strong>
            <span>{t.brandSubtitle}</span>
          </div>
        </div>
        <nav>
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <button key={item.id} className={activeView === item.id ? "active" : ""} onClick={() => setActiveView(item.id)}>
                <Icon size={17} />
                {t.nav[item.id]}
              </button>
            );
          })}
        </nav>
      </aside>

      <section className="workspace">
        <header className="topbar">
          <div>
            <span className="eyebrow">{t.platform}</span>
            <h1>{t.titles[activeView]}</h1>
          </div>
          <div className="topbar-actions">
            <div className="language-toggle" aria-label={t.language}>
              {(Object.keys(locales) as Locale[]).map((item) => (
                <button key={item} className={locale === item ? "active" : ""} onClick={() => setLocale(item)}>
                  {item.toUpperCase()}
                </button>
              ))}
            </div>
            <div className="language-toggle" aria-label="Currency">
              {(["GBP", "EUR"] as Currency[]).map((item) => (
                <button key={item} className={currency === item ? "active" : ""} onClick={() => setCurrency(item)}>
                  {item}
                </button>
              ))}
            </div>
            <div className="api-pill">{t.api}</div>
          </div>
        </header>

        {error ? <ApiError message={error} locale={locale} /> : null}
        {!data && !error ? <LoadingState locale={locale} /> : null}
        {data ? (
          <>
            {activeView === "overview" ? <Overview data={data} locale={locale} currency={currency} sourceCurrency={sourceCurrency(data)} /> : null}
            {activeView === "data" ? <DataManager labels={t.data} currency={currency} setCurrency={setCurrency} onRefresh={loadData} /> : null}
            {activeView === "customers" ? <Customers data={data} locale={locale} currency={currency} sourceCurrency={sourceCurrency(data)} /> : null}
            {activeView === "segments" ? (
              <Segments
                segments={data.segments}
                selectedSegment={selectedSegment}
                selectedSegmentData={selectedSegmentData}
                recommendation={selectedRecommendation}
                onSelect={setSelectedSegment}
                locale={locale}
                currency={currency}
                sourceCurrency={sourceCurrency(data)}
              />
            ) : null}
            {activeView === "clustering" ? <Clustering data={data} locale={locale} currency={currency} sourceCurrency={sourceCurrency(data)} /> : null}
            {activeView === "campaigns" ? <Campaigns data={data} locale={locale} currency={currency} sourceCurrency={sourceCurrency(data)} /> : null}
            {activeView === "insights" ? <Insights insights={data.insights} locale={locale} currency={currency} sourceCurrency={sourceCurrency(data)} /> : null}
            {activeView === "methodology" ? <Methodology data={data} locale={locale} /> : null}
          </>
        ) : null}
      </section>
    </main>
  );
}

function sourceCurrency(data: AppData): Currency {
  return data.summary.source_currency === "EUR" ? "EUR" : "GBP";
}

function Overview({ data, locale, currency, sourceCurrency }: { data: AppData; locale: Locale; currency: Currency; sourceCurrency: Currency }) {
  const summary = data.summary;
  const t = copy[locale];
  return (
    <div className="view-stack">
      <section className="metrics-grid">
        <DashboardCard label={t.overview.totalCustomers} value={summary.total_customers.toLocaleString()} detail={t.overview.rfmProfiles} tone="blue" />
        <DashboardCard label={t.overview.revenue} value={formatCurrency(summary.total_revenue, currency, sourceCurrency)} detail={t.overview.cleanedTransactions} tone="green" />
        <DashboardCard label={t.overview.orders} value={summary.total_orders.toLocaleString()} detail={t.overview.uniqueInvoices} tone="cyan" />
        <DashboardCard label={t.overview.avgOrderValue} value={formatCurrency(summary.avg_order_value, currency, sourceCurrency)} detail={t.overview.perInvoice} tone="orange" />
        <DashboardCard label={t.overview.activeCustomers} value={summary.active_customers.toLocaleString()} detail={t.overview.activeDetail} tone="green" />
        <DashboardCard label={t.overview.inactiveCustomers} value={summary.inactive_customers.toLocaleString()} detail={t.overview.inactiveDetail} tone="red" />
      </section>
      <RevenueChart
        data={data.revenue}
        title={t.revenueChart.title}
        subtitle={t.revenueChart.periods}
        tooltipLabel={t.revenueChart.tooltip}
        currency={currency}
        sourceCurrency={sourceCurrency}
      />
      <section className="two-column">
        <div className="chart-panel">
          <div className="section-heading">
            <h2>{t.overview.revenueBySegment}</h2>
            <span>{t.overview.monetaryShare}</span>
          </div>
          <div className="chart-height short">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={data.segments} dataKey="total_revenue" nameKey="segment" outerRadius={92} innerRadius={52}>
                  {data.segments.map((_, index) => (
                    <Cell key={index} fill={segmentColors[index % segmentColors.length]} />
                  ))}
                </Pie>
                <Tooltip formatter={(value) => [formatCurrency(Number(value), currency, sourceCurrency), t.overview.revenue]} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
        <div className="chart-panel">
          <div className="section-heading">
            <h2>{t.overview.customerDistribution}</h2>
            <span>{t.overview.segmentSize}</span>
          </div>
          <div className="chart-height short">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data.segments} layout="vertical">
                <CartesianGrid stroke="#E5E0D8" strokeDasharray="3 3" />
                <XAxis type="number" tick={{ fontSize: 12 }} />
                <YAxis
                  dataKey="segment"
                  type="category"
                  width={122}
                  tick={{ fontSize: 11 }}
                  tickFormatter={(value) => segmentLabel(String(value), locale)}
                />
                <Tooltip formatter={(value) => [Number(value).toLocaleString(), t.segments.customers]} />
                <Bar dataKey="count" radius={[0, 6, 6, 0]}>
                  {data.segments.map((_, index) => (
                    <Cell key={index} fill={segmentColors[index % segmentColors.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </section>
    </div>
  );
}

function Customers({ data, locale, currency, sourceCurrency }: { data: AppData; locale: Locale; currency: Currency; sourceCurrency: Currency }) {
  const t = copy[locale];
  return (
    <div className="view-stack">
      <div className="section-heading">
        <h2>{t.customers.title}</h2>
        <span>
          {data.customers.total.toLocaleString()} {t.customers.available}
        </span>
      </div>
      <CustomerTable customers={data.customers.data} locale={locale} labels={t.customers} currency={currency} sourceCurrency={sourceCurrency} />
    </div>
  );
}

function Segments({
  segments,
  selectedSegment,
  selectedSegmentData,
  recommendation,
  onSelect,
  locale,
  currency,
  sourceCurrency,
}: {
  segments: SegmentSummary[];
  selectedSegment: string | null;
  selectedSegmentData: SegmentSummary | null;
  recommendation: CampaignRecommendation | null;
  onSelect: (segment: string) => void;
  locale: Locale;
  currency: Currency;
  sourceCurrency: Currency;
}) {
  const t = copy[locale];
  return (
    <div className="view-stack">
      <section className="segment-grid">
        {segments.map((segment) => (
          <SegmentCard
            key={segment.segment}
            segment={segment}
            selected={selectedSegment === segment.segment}
            onSelect={onSelect}
            locale={locale}
            revenueLabel={t.segments.revenueLabel}
            shareLabel={t.segments.share}
            currency={currency}
            sourceCurrency={sourceCurrency}
          />
        ))}
      </section>
      {selectedSegmentData ? (
        <section className="detail-band">
          <div>
            <span className={`segment-dot ${segmentClass(selectedSegmentData.segment)}`} />
            <h2>{segmentLabel(selectedSegmentData.segment, locale)}</h2>
            <p>{segmentDescription(selectedSegmentData.segment, selectedSegmentData.description ?? "", locale)}</p>
          </div>
          <div className="result-grid">
            <div>
              <span>{t.segments.customers}</span>
              <strong>{selectedSegmentData.count.toLocaleString()}</strong>
            </div>
            <div>
              <span>{t.segments.revenue}</span>
              <strong>{formatCurrency(selectedSegmentData.total_revenue, currency, sourceCurrency)}</strong>
            </div>
            <div>
              <span>{t.segments.avgRecency}</span>
              <strong>{formatNumber(selectedSegmentData.avg_recency)}d</strong>
            </div>
            <div>
              <span>{t.segments.avgFrequency}</span>
              <strong>{formatNumber(selectedSegmentData.avg_frequency)}x</strong>
            </div>
          </div>
          {recommendation ? (
            <div className="campaign-list">
              {recommendation.campaigns.map((campaign) => (
                <article key={campaign.type}>
                  <strong>{campaignLabel(campaign.type, locale)}</strong>
                  <span>{campaignObjective(campaign.objective, locale)}</span>
                  <small>{campaignMessage(campaign.type, campaign.message, locale)}</small>
                </article>
              ))}
            </div>
          ) : null}
        </section>
      ) : null}
    </div>
  );
}

function Clustering({ data, locale, currency, sourceCurrency }: { data: AppData; locale: Locale; currency: Currency; sourceCurrency: Currency }) {
  const t = copy[locale];
  return (
    <div className="view-stack">
      <section className="metrics-grid compact">
        <DashboardCard label={t.clustering.clusters} value={String(data.metrics.n_clusters)} detail={t.clustering.kmeansGroups} tone="blue" />
        <DashboardCard label={t.clustering.silhouette} value={String(data.metrics.silhouette_score)} detail={t.clustering.clusterSeparation} tone="green" />
        <DashboardCard label={t.clustering.inertia} value={formatNumber(data.metrics.inertia)} detail={t.clustering.variance} tone="orange" />
      </section>
      <ClusterScatterPlot points={data.clusterPoints} title={t.clustering.title} subtitle={t.clustering.subtitle} revenueLabel={t.clustering.revenue} currency={currency} sourceCurrency={sourceCurrency} />
    </div>
  );
}

function Campaigns({ data, locale, currency, sourceCurrency }: { data: AppData; locale: Locale; currency: Currency; sourceCurrency: Currency }) {
  const t = copy[locale];
  return (
    <div className="view-stack">
      <CampaignSimulator segments={data.segments} locale={locale} labels={t.campaigns} currency={currency} sourceCurrency={sourceCurrency} />
      <section className="campaign-list">
        {data.recommendations.map((recommendation) => (
          <article key={recommendation.segment}>
            <strong>{segmentLabel(recommendation.segment, locale)}</strong>
            <span>{businessGoal(recommendation.segment, recommendation.business_goal, locale)}</span>
            <small>{recommendation.campaigns.map((campaign) => campaignLabel(campaign.type, locale)).join(", ")}</small>
          </article>
        ))}
      </section>
    </div>
  );
}

function Insights({ insights, locale, currency, sourceCurrency }: { insights: Insight[]; locale: Locale; currency: Currency; sourceCurrency: Currency }) {
  const t = copy[locale];
  return (
    <section className="insight-grid">
      {insights.map((insight) => (
        <InsightCard key={insight.id} insight={insight} locale={locale} actionLabel={t.insights.action} impactLabel={t.insights.impact} currency={currency} sourceCurrency={sourceCurrency} />
      ))}
    </section>
  );
}

function Methodology({ data, locale }: { data: AppData; locale: Locale }) {
  const t = copy[locale];
  return (
    <div className="method-grid">
      {t.methodology.steps.map((step, index) => (
        <article key={step.title}>
          <span className="eyebrow">{step.eyebrow}</span>
          <h3>{step.title}</h3>
          <p>
            {step.text}
            {index === 2 ? ` ${data.metrics.silhouette_score}.` : ""}
          </p>
        </article>
      ))}
    </div>
  );
}

function LoadingState({ locale }: { locale: Locale }) {
  return (
    <div className="loading-state">
      <Loader2 className="spin" size={22} />
      {copy[locale].states.loading}
    </div>
  );
}

function ApiError({ message, locale }: { message: string; locale: Locale }) {
  const t = copy[locale];
  return (
    <div className="error-state">
      <strong>{t.states.backendTitle}</strong>
      <span>{message}</span>
      <span>{t.states.backendCommand}</span>
      <code>cd files\backend && ..\..\.venv311\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000</code>
    </div>
  );
}

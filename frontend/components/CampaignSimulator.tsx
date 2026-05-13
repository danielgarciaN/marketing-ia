"use client";

import { useState } from "react";
import { Play } from "lucide-react";
import { api } from "@/lib/api";
import type { CampaignSimulationResult, SegmentSummary } from "@/lib/types";
import { formatCurrency } from "@/lib/format";
import type { Locale } from "@/lib/i18n";
import { campaignLabel, segmentLabel } from "@/lib/i18n";

const campaignTypes = ["email", "sms", "push", "direct_mail", "retargeting"];

export function CampaignSimulator({
  segments,
  locale,
  labels,
}: {
  segments: SegmentSummary[];
  locale: Locale;
  labels: {
    segment: string;
    campaignType: string;
    budget: string;
    discount: string;
    conversion: string;
    simulate: string;
    simulating: string;
    estimatedRevenue: string;
    roi: string;
    customersReached: string;
    conversions: string;
    empty: string;
  };
}) {
  const [segment, setSegment] = useState(segments[0]?.segment ?? "");
  const [campaignType, setCampaignType] = useState("email");
  const [budget, setBudget] = useState(1000);
  const [discountPct, setDiscountPct] = useState(15);
  const [conversionRate, setConversionRate] = useState(5);
  const [result, setResult] = useState<CampaignSimulationResult | null>(null);
  const [loading, setLoading] = useState(false);

  const runSimulation = async () => {
    if (!segment) return;
    setLoading(true);
    try {
      const response = await api.simulateCampaign({
        segment,
        campaign_type: campaignType,
        budget,
        discount_pct: discountPct,
        expected_conversion_rate: conversionRate,
      });
      setResult(response);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="simulator-grid">
      <div className="control-panel">
        <label>
          {labels.segment}
          <select value={segment} onChange={(event) => setSegment(event.target.value)}>
            {segments.map((item) => (
              <option key={item.segment} value={item.segment}>
                {segmentLabel(item.segment, locale)}
              </option>
            ))}
          </select>
        </label>
        <label>
          {labels.campaignType}
          <select value={campaignType} onChange={(event) => setCampaignType(event.target.value)}>
            {campaignTypes.map((item) => (
              <option key={item} value={item}>
                {campaignLabel(item, locale)}
              </option>
            ))}
          </select>
        </label>
        <label>
          {labels.budget}
          <input type="number" min="0" value={budget} onChange={(event) => setBudget(Number(event.target.value))} />
        </label>
        <label>
          {labels.discount}
          <input type="number" min="0" max="90" value={discountPct} onChange={(event) => setDiscountPct(Number(event.target.value))} />
        </label>
        <label>
          {labels.conversion}
          <input type="number" min="0" max="100" value={conversionRate} onChange={(event) => setConversionRate(Number(event.target.value))} />
        </label>
        <button className="primary-button" onClick={runSimulation} disabled={loading}>
          <Play size={16} />
          {loading ? labels.simulating : labels.simulate}
        </button>
      </div>

      <div className="result-panel">
        {result ? (
          <>
            <div className="result-grid">
              <div>
                <span>{labels.estimatedRevenue}</span>
                <strong>{formatCurrency(result.estimated_revenue)}</strong>
              </div>
              <div>
                <span>{labels.roi}</span>
                <strong>{result.roi_pct}%</strong>
              </div>
              <div>
                <span>{labels.customersReached}</span>
                <strong>{result.customers_reached.toLocaleString()}</strong>
              </div>
              <div>
                <span>{labels.conversions}</span>
                <strong>{result.expected_conversions.toLocaleString()}</strong>
              </div>
            </div>
            <p className="recommendation">{simulationRecommendation(result, locale)}</p>
          </>
        ) : (
          <div className="empty-state">{labels.empty}</div>
        )}
      </div>
    </section>
  );
}

function simulationRecommendation(result: CampaignSimulationResult, locale: Locale) {
  if (locale === "en") return result.recommendation;

  const segment = segmentLabel(result.segment, locale);
  const channel = campaignLabel(result.campaign_type, locale);

  if (result.roi_pct > 200) {
    return `ROI excelente previsto. Se recomienda lanzar la campaña de ${channel} para ${segment} y valorar un aumento de presupuesto.`;
  }
  if (result.roi_pct > 50) {
    return `ROI positivo esperado. La campaña de ${channel} para ${segment} es viable; conviene monitorizar resultados y optimizar.`;
  }
  if (result.roi_pct > 0) {
    return `ROI positivo pero ajustado. Recomendable hacer un A/B test antes de escalar la campaña para ${segment}.`;
  }
  return `ROI negativo previsto para ${segment} con ${channel}. Conviene revisar canal, descuento o propuesta de valor.`;
}

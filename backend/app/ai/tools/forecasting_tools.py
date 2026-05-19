"""Forecasting tools — statistical projections built on existing pipeline data."""
from __future__ import annotations

import math
from typing import Any
from langchain_core.tools import tool

from app.services.data_service import DataService


def _load():
    svc = DataService()
    svc.load()
    return svc


@tool
def forecast_revenue(horizon_months: int = 3) -> dict[str, Any]:
    """Forecast future monthly revenue using linear trend extrapolation.

    Args:
        horizon_months: Number of months to project forward (1–12).
    """
    horizon_months = max(1, min(horizon_months, 12))
    svc = _load()

    history = svc.revenue_monthly or []
    if len(history) < 2:
        return {"error": "Insufficient historical data for forecasting."}

    revenues = [float(r.get("revenue", 0)) for r in history if "revenue" in r]
    n = len(revenues)
    x_mean = (n - 1) / 2
    y_mean = sum(revenues) / n
    num = sum((i - x_mean) * (revenues[i] - y_mean) for i in range(n))
    den = sum((i - x_mean) ** 2 for i in range(n))
    slope = num / den if den else 0
    intercept = y_mean - slope * x_mean

    forecast = []
    for h in range(1, horizon_months + 1):
        projected = intercept + slope * (n - 1 + h)
        forecast.append({"month_offset": h, "projected_revenue": round(max(projected, 0), 2)})

    total_projected = sum(f["projected_revenue"] for f in forecast)
    growth_rate = slope / max(y_mean, 1) * 100

    return {
        "model": "linear_trend",
        "horizon_months": horizon_months,
        "historical_avg_monthly_revenue": round(y_mean, 2),
        "monthly_growth_rate_pct": round(growth_rate, 2),
        "forecast": forecast,
        "total_projected_revenue": round(total_projected, 2),
        "confidence": "medium" if n >= 6 else "low",
    }


@tool
def predict_churn_risk(segment: str | None = None) -> dict[str, Any]:
    """Estimate churn risk for a segment or the entire base using recency heuristics.

    Returns: risk_level (low/medium/high), at_risk_count, churn_rate_estimate.
    """
    svc = _load()
    df = svc.customers
    if df is None:
        return {"error": "No customer data available."}

    if segment:
        df = df[df.get("Segment", df.get("segment", "")) == segment]  # type: ignore

    recency_col = next((c for c in ["Recency", "recency", "R_Score"] if c in df.columns), None)
    if recency_col is None:
        return {"error": "Recency column not found."}

    total = len(df)
    if recency_col == "R_Score":
        at_risk = int((df[recency_col] <= 2).sum())
    else:
        at_risk = int((df[recency_col] > 90).sum())

    churn_rate = round(at_risk / max(total, 1) * 100, 2)
    risk_level = "high" if churn_rate > 40 else ("medium" if churn_rate > 20 else "low")

    return {
        "segment": segment or "all",
        "total_customers": total,
        "at_risk_count": at_risk,
        "churn_rate_estimate_pct": churn_rate,
        "risk_level": risk_level,
        "recommendation": (
            "Urgente: lanzar campaña de reactivación inmediata." if risk_level == "high"
            else "Considerar campaña de retención preventiva." if risk_level == "medium"
            else "Base saludable, mantener programa de fidelización."
        ),
    }


@tool
def estimate_ltv(segment: str | None = None, projection_months: int = 12) -> dict[str, Any]:
    """Estimate Customer Lifetime Value (LTV) for a segment over a projection period."""
    svc = _load()
    df = svc.customers
    if df is None:
        return {"error": "No customer data available."}

    if segment:
        df = df[df.get("Segment", "") == segment]

    monetary_col = next((c for c in ["Monetary", "monetary"] if c in df.columns), None)
    freq_col = next((c for c in ["Frequency", "frequency"] if c in df.columns), None)

    if monetary_col is None or freq_col is None:
        return {"error": "Required columns (Monetary, Frequency) not found."}

    avg_order_value = float(df[monetary_col].mean() / df[freq_col].mean())
    avg_purchase_freq = float(df[freq_col].mean()) / 12
    margin_rate = 0.30
    churn_rate_monthly = 0.05

    ltv = (avg_order_value * avg_purchase_freq * margin_rate) / max(churn_rate_monthly, 0.001)

    return {
        "segment": segment or "all",
        "projection_months": projection_months,
        "avg_order_value": round(avg_order_value, 2),
        "avg_monthly_purchase_freq": round(avg_purchase_freq, 3),
        "estimated_ltv": round(ltv, 2),
        "total_segment_ltv": round(ltv * len(df), 2),
        "model": "basic_ltv_margin",
    }

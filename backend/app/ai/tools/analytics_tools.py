"""Analytical tools — Pandas-powered computation on top of the in-memory dataset."""
from __future__ import annotations

from typing import Any
import pandas as pd
from langchain_core.tools import tool

from app.services.data_service import DataService


def _df() -> pd.DataFrame:
    svc = DataService()
    svc.load()
    return svc.customers  # type: ignore[return-value]


@tool
def compute_segment_stats(segment: str) -> dict[str, Any]:
    """Compute detailed statistics for a specific segment: revenue share, churn risk, avg LTV."""
    df = _df()
    subset = df[df["Segment"] == segment] if "Segment" in df.columns else pd.DataFrame()
    if subset.empty:
        return {"error": f"No data for segment '{segment}'."}

    monetary_col = next((c for c in ["Monetary", "monetary", "TotalSpend"] if c in subset.columns), None)
    recency_col = next((c for c in ["Recency", "recency"] if c in subset.columns), None)
    freq_col = next((c for c in ["Frequency", "frequency"] if c in subset.columns), None)

    stats: dict[str, Any] = {
        "segment": segment,
        "customer_count": int(len(subset)),
        "pct_of_total": round(len(subset) / max(len(df), 1) * 100, 2),
    }
    if monetary_col:
        stats["total_revenue"] = round(float(subset[monetary_col].sum()), 2)
        stats["avg_monetary"] = round(float(subset[monetary_col].mean()), 2)
        stats["median_monetary"] = round(float(subset[monetary_col].median()), 2)
    if recency_col:
        stats["avg_recency_days"] = round(float(subset[recency_col].mean()), 1)
    if freq_col:
        stats["avg_frequency"] = round(float(subset[freq_col].mean()), 2)

    return stats


@tool
def run_pandas_query(filter_expression: str, columns: list[str] | None = None) -> list[dict[str, Any]]:
    """Execute a Pandas query string against the customer dataset and return matching rows.

    Args:
        filter_expression: Valid pandas query string, e.g. "Monetary > 500 and Recency < 30"
        columns: Optional list of columns to include in the output.
    """
    df = _df()
    try:
        result = df.query(filter_expression)
    except Exception as exc:
        return [{"error": f"Invalid query: {exc}"}]

    if columns:
        valid_cols = [c for c in columns if c in result.columns]
        result = result[valid_cols]

    return result.head(200).to_dict(orient="records")


@tool
def get_rfm_distribution() -> dict[str, Any]:
    """Return score distribution histograms for Recency, Frequency, and Monetary."""
    df = _df()
    result: dict[str, Any] = {}
    for col in ["R_Score", "F_Score", "M_Score", "RFM_Score"]:
        if col in df.columns:
            dist = df[col].value_counts().sort_index()
            result[col] = dist.to_dict()
    return result


@tool
def get_revenue_trend() -> list[dict[str, Any]]:
    """Return monthly revenue time series from the processed pipeline output."""
    from app.services.data_service import DataService
    svc = DataService()
    svc.load()
    if svc.revenue_monthly is None:
        return []
    if isinstance(svc.revenue_monthly, list):
        return svc.revenue_monthly
    if hasattr(svc.revenue_monthly, "to_dict"):
        return svc.revenue_monthly.to_dict(orient="records")
    return []

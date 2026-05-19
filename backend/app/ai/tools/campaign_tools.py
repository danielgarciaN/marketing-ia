"""Campaign tools — wrappers over existing recommendation and simulation services."""
from __future__ import annotations

from typing import Any, Literal
from langchain_core.tools import tool

from app.services.recommendation_service import get_all_recommendations
from app.services.campaign_simulator_service import simulate_campaign as _simulate
from app.services.data_service import DataService


@tool
def get_campaign_recommendations(segment: str | None = None) -> list[dict[str, Any]]:
    """Return campaign playbooks. Optionally filter to a specific segment.
    Each playbook contains: segment, description, business_goal, campaigns list.
    """
    all_recs = get_all_recommendations()
    if segment:
        return [r for r in all_recs if r.get("segment", "").lower() == segment.lower()]
    return all_recs


@tool
def simulate_campaign(
    segment: str,
    campaign_type: str,
    budget: float,
    discount_pct: float = 0.0,
    expected_conversion_rate: float = 0.05,
) -> dict[str, Any]:
    """Simulate a marketing campaign and return projected ROI metrics.

    Args:
        segment: Target segment name (e.g. 'At-Risk', 'VIP Customers')
        campaign_type: Campaign type (e.g. 'Email', 'Discount', 'Win-Back')
        budget: Total campaign budget in base currency
        discount_pct: Discount percentage offered (0-100)
        expected_conversion_rate: Fraction of reached customers expected to convert (0-1)
    """
    result = _simulate(
        segment=segment,
        campaign_type=campaign_type,
        budget=budget,
        discount_pct=discount_pct,
        expected_conversion_rate=expected_conversion_rate,
    )
    return result if isinstance(result, dict) else result.dict()


@tool
def rank_segments_by_opportunity(
    metric: Literal["revenue", "size", "risk"] = "revenue",
    top_n: int = 3,
) -> list[dict[str, Any]]:
    """Rank customer segments by opportunity metric: revenue potential, segment size, or churn risk.

    Returns top_n segments with supporting stats.
    """
    svc = DataService()
    svc.load()

    segments = svc.segment_summary
    if segments is None:
        return []

    import pandas as pd
    if isinstance(segments, list):
        df = pd.DataFrame(segments)
    else:
        df = segments.copy()

    col_map = {
        "revenue": ["total_revenue", "TotalRevenue", "revenue"],
        "size": ["customer_count", "Count", "count"],
        "risk": ["avg_recency_days", "Recency", "recency"],
    }
    sort_col = next((c for c in col_map[metric] if c in df.columns), None)
    if sort_col is None:
        return df.head(top_n).to_dict(orient="records")

    ascending = metric == "risk"
    ranked = df.sort_values(sort_col, ascending=ascending).head(top_n)
    return ranked.to_dict(orient="records")

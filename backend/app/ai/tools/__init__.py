"""Reusable tool registry for all agents."""
from app.ai.tools.data_tools import (
    get_dashboard_summary,
    get_customer_by_id,
    get_customers_by_segment,
    get_segment_overview,
)
from app.ai.tools.analytics_tools import (
    compute_segment_stats,
    run_pandas_query,
    get_rfm_distribution,
    get_revenue_trend,
)
from app.ai.tools.campaign_tools import (
    get_campaign_recommendations,
    simulate_campaign,
    rank_segments_by_opportunity,
)
from app.ai.tools.forecasting_tools import (
    forecast_revenue,
    predict_churn_risk,
    estimate_ltv,
)
from app.ai.tools.report_tools import (
    generate_executive_summary,
    format_insights_report,
)
from app.ai.tools.rag_tools import retrieve_marketing_knowledge

__all__ = [
    "get_dashboard_summary",
    "get_customer_by_id",
    "get_customers_by_segment",
    "get_segment_overview",
    "compute_segment_stats",
    "run_pandas_query",
    "get_rfm_distribution",
    "get_revenue_trend",
    "get_campaign_recommendations",
    "simulate_campaign",
    "rank_segments_by_opportunity",
    "forecast_revenue",
    "predict_churn_risk",
    "estimate_ltv",
    "generate_executive_summary",
    "format_insights_report",
    "retrieve_marketing_knowledge",
]

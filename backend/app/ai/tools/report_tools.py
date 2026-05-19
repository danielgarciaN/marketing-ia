"""Report generation tools — structure and format multi-agent outputs."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from langchain_core.tools import tool


@tool
def generate_executive_summary(
    analysis_results: dict[str, Any],
    recommendations: list[dict[str, Any]],
    forecast_data: dict[str, Any],
) -> str:
    """Generate a structured executive summary from agent outputs.

    Combines analysis, recommendations and forecasts into a coherent business narrative.
    Returns formatted markdown text.
    """
    lines: list[str] = ["# Executive Summary\n"]
    lines.append(f"_Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}_\n")

    if analysis_results:
        lines.append("## Business Overview")
        for key, value in analysis_results.items():
            label = key.replace("_", " ").title()
            lines.append(f"- **{label}**: {value}")
        lines.append("")

    if recommendations:
        lines.append("## Top Recommendations")
        for i, rec in enumerate(recommendations[:3], 1):
            segment = rec.get("segment", "N/A")
            campaign = rec.get("campaign_type", rec.get("type", "N/A"))
            roi = rec.get("roi_pct", rec.get("roi", "N/A"))
            lines.append(f"{i}. **{segment}** — {campaign} (ROI estimado: {roi}%)")
        lines.append("")

    if forecast_data and "forecast" in forecast_data:
        lines.append("## Revenue Forecast")
        for entry in forecast_data["forecast"][:3]:
            offset = entry.get("month_offset", "?")
            revenue = entry.get("projected_revenue", "?")
            lines.append(f"- Mes +{offset}: **{revenue:,.0f}**" if isinstance(revenue, float) else f"- Mes +{offset}: {revenue}")
        lines.append("")

    return "\n".join(lines)


@tool
def format_insights_report(insights: list[dict[str, Any]], language: str = "es") -> str:
    """Format a list of business insights into a readable markdown report.

    Args:
        insights: List of insight dicts with keys: title, insight, action, priority, category.
        language: Output language code ('es' or 'en').
    """
    if not insights:
        return "No insights available." if language == "en" else "No hay insights disponibles."

    header = "## Key Insights" if language == "en" else "## Insights Clave"
    lines = [header, ""]

    priority_map = {"high": "🔴", "medium": "🟡", "low": "🟢"}
    for insight in insights:
        icon = priority_map.get(insight.get("priority", "low"), "⚪")
        title = insight.get("title", "Insight")
        body = insight.get("insight", "")
        action = insight.get("action", "")
        lines.append(f"### {icon} {title}")
        if body:
            lines.append(body)
        if action:
            action_label = "**Action:**" if language == "en" else "**Acción:**"
            lines.append(f"\n{action_label} _{action}_")
        lines.append("")

    return "\n".join(lines)

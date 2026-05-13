"""
Automatic business insight generation using rules-based logic.
"""
from app.services.data_service import data_service


def generate_insights() -> list:
    """Generate actionable business insights from customer data."""
    data_service.load()
    customers = data_service.customers
    segments = data_service.segment_summary
    summary = data_service.dashboard_summary

    insights = []

    # --- VIP Revenue Concentration ---
    vip = next((s for s in segments if s["segment"] == "VIP Customers"), None)
    if vip:
        insights.append({
            "id": "vip_concentration",
            "category": "Revenue",
            "title": "VIP Revenue Concentration",
            "insight": f"VIP Customers represent {vip['pct_customers']}% of the customer base but generate {vip['pct_revenue']}% of total revenue (£{vip['total_revenue']:,.0f}). Prioritize retention campaigns and exclusive benefits for this segment.",
            "priority": "Critical",
            "action": "Launch a VIP loyalty program with early access, premium support, and personalized offers.",
            "impact": "High",
        })

    # --- At-Risk Alert ---
    at_risk = next((s for s in segments if s["segment"] == "At-Risk Customers"), None)
    if at_risk:
        insights.append({
            "id": "at_risk_alert",
            "category": "Retention",
            "title": "At-Risk Customer Alert",
            "insight": f"{at_risk['count']} customers ({at_risk['pct_customers']}%) are at risk of churn. They have an average frequency of {at_risk['avg_frequency']:.1f} orders but haven't purchased in {at_risk['avg_recency']:.0f} days. Historical average spend: £{at_risk['avg_monetary']:,.0f}.",
            "priority": "Critical",
            "action": "Deploy a reactivation campaign with personalized discounts (15-20%) and urgency-driven messaging within the next 7 days.",
            "impact": "High",
        })

    # --- New Customer Conversion ---
    new = next((s for s in segments if s["segment"] == "New Customers"), None)
    if new:
        insights.append({
            "id": "new_conversion",
            "category": "Growth",
            "title": "New Customer Conversion Opportunity",
            "insight": f"{new['count']} new customers have joined recently with an average order value of £{new['avg_order_value']:.0f}. The window to convert them into repeat buyers is typically 30 days.",
            "priority": "High",
            "action": "Set up an automated onboarding email series with product recommendations and a second-purchase incentive.",
            "impact": "Medium",
        })

    # --- Lost Customer Recovery ---
    lost = next((s for s in segments if s["segment"] == "Lost Customers"), None)
    if lost:
        insights.append({
            "id": "lost_recovery",
            "category": "Retention",
            "title": "Lost Customer Recovery Potential",
            "insight": f"{lost['count']} customers are classified as lost ({lost['pct_customers']}% of total base). Their combined historical revenue was £{lost['total_revenue']:,.0f}. Even a 5% reactivation rate would recover £{lost['total_revenue'] * 0.05:,.0f}.",
            "priority": "Medium",
            "action": "Run a win-back campaign with a strong incentive (25-30% discount or free shipping) as a last-effort recovery.",
            "impact": "Medium",
        })

    # --- Revenue Trend ---
    revenue_data = data_service.revenue_monthly
    if len(revenue_data) >= 3:
        last_3 = [r["revenue"] for r in revenue_data[-3:]]
        trend = "growing" if last_3[-1] > last_3[0] else "declining"
        pct_change = ((last_3[-1] - last_3[0]) / last_3[0] * 100) if last_3[0] > 0 else 0
        insights.append({
            "id": "revenue_trend",
            "category": "Revenue",
            "title": "Revenue Trend Analysis",
            "insight": f"Revenue over the last 3 months is {trend} ({pct_change:+.1f}%). Latest month: £{last_3[-1]:,.0f}. The overall trend suggests {'positive momentum' if trend == 'growing' else 'the need for intervention to reverse the decline'}.",
            "priority": "High" if trend == "declining" else "Medium",
            "action": f"{'Scale up successful campaigns and increase acquisition spend.' if trend == 'growing' else 'Investigate churn drivers. Consider promotional campaigns targeting At-Risk and Occasional segments.'}",
            "impact": "High",
        })

    # --- High Potential Upsell ---
    hp = next((s for s in segments if s["segment"] == "High Potential"), None)
    if hp:
        insights.append({
            "id": "high_potential_upsell",
            "category": "Growth",
            "title": "High Potential Upsell Opportunity",
            "insight": f"{hp['count']} customers show high potential with an average spend of £{hp['avg_monetary']:,.0f} and good recency ({hp['avg_recency']:.0f} days). Cross-selling and upselling strategies could increase their lifetime value significantly.",
            "priority": "High",
            "action": "Implement personalized product recommendations and bundle offers for this segment.",
            "impact": "High",
        })

    # --- Geographic Concentration ---
    top_country = summary.get("top_country", "Unknown")
    uk_pct = len(customers[customers["Country"] == "United Kingdom"]) / len(customers) * 100
    insights.append({
        "id": "geo_concentration",
        "category": "Strategy",
        "title": "Geographic Concentration Risk",
        "insight": f"{uk_pct:.0f}% of customers are from {top_country}. This concentration creates market risk. International customers often have higher AOV and present diversification opportunities.",
        "priority": "Low",
        "action": "Explore targeted campaigns for top international markets (Germany, France, Spain) to diversify the customer base.",
        "impact": "Medium",
    })

    # --- Frequency Gap ---
    avg_freq = customers["Frequency"].mean()
    median_freq = customers["Frequency"].median()
    insights.append({
        "id": "frequency_gap",
        "category": "Engagement",
        "title": "Purchase Frequency Gap",
        "insight": f"Average purchase frequency is {avg_freq:.1f} orders but the median is {median_freq:.0f}, indicating a skewed distribution where a few high-frequency customers pull the average up. Most customers buy only {median_freq:.0f} times.",
        "priority": "Medium",
        "action": "Design frequency-boosting programs (subscription models, loyalty points, replenishment reminders) targeting customers with 1-3 purchases.",
        "impact": "High",
    })

    return insights

"""
Campaign simulation: estimate ROI, uplift, and impact of marketing campaigns.
"""
from app.services.data_service import data_service


CONVERSION_MULTIPLIERS = {
    "VIP Customers": 1.5,
    "Loyal Customers": 1.3,
    "New Customers": 0.8,
    "At-Risk Customers": 0.6,
    "Lost Customers": 0.3,
    "Occasional Buyers": 0.7,
    "High Potential": 1.1,
}

CAMPAIGN_COSTS = {
    "email": 0.15,        # per customer
    "sms": 0.25,
    "push": 0.05,
    "direct_mail": 2.50,
    "retargeting": 0.80,
}


def simulate_campaign(
    segment: str,
    campaign_type: str = "email",
    budget: float = 1000.0,
    discount_pct: float = 10.0,
    expected_conversion_rate: float = 5.0,
) -> dict:
    """Simulate campaign impact for a given segment."""
    data_service.load()
    customers = data_service.customers

    seg_data = customers[customers["Segment"] == segment]
    if seg_data.empty:
        return {"error": f"Segment '{segment}' not found"}

    n_customers = len(seg_data)
    avg_monetary = seg_data["Monetary"].mean()
    avg_order_value = seg_data["AvgOrderValue"].mean()

    # Adjust conversion based on segment
    multiplier = CONVERSION_MULTIPLIERS.get(segment, 1.0)
    adjusted_conversion = min(expected_conversion_rate * multiplier, 100.0) / 100.0

    # Cost per customer
    cost_per_customer = CAMPAIGN_COSTS.get(campaign_type, 0.15)
    total_cost = min(n_customers * cost_per_customer, budget)
    customers_reached = int(total_cost / cost_per_customer) if cost_per_customer > 0 else n_customers

    # Expected conversions
    conversions = int(customers_reached * adjusted_conversion)

    # Revenue estimation
    discount_factor = 1 - (discount_pct / 100)
    revenue_per_conversion = avg_order_value * discount_factor
    estimated_revenue = round(conversions * revenue_per_conversion, 2)

    # ROI
    campaign_cost = total_cost + (conversions * avg_order_value * (discount_pct / 100))
    roi = round(((estimated_revenue - campaign_cost) / campaign_cost * 100), 1) if campaign_cost > 0 else 0

    # Uplift vs no campaign
    baseline_conversions = int(customers_reached * 0.01)  # 1% organic
    uplift = conversions - baseline_conversions

    return {
        "segment": segment,
        "campaign_type": campaign_type,
        "budget": budget,
        "discount_pct": discount_pct,
        "customers_in_segment": n_customers,
        "customers_reached": customers_reached,
        "adjusted_conversion_rate": round(adjusted_conversion * 100, 1),
        "expected_conversions": conversions,
        "estimated_revenue": estimated_revenue,
        "campaign_cost": round(campaign_cost, 2),
        "roi_pct": roi,
        "uplift_conversions": uplift,
        "avg_order_value": round(avg_order_value, 2),
        "recommendation": _generate_recommendation(segment, roi, conversions, campaign_type),
    }


def _generate_recommendation(segment: str, roi: float, conversions: int, campaign_type: str) -> str:
    if roi > 200:
        return f"Excellent ROI projected. Strongly recommend launching this {campaign_type} campaign for {segment}. Consider increasing budget."
    elif roi > 50:
        return f"Good ROI expected. This {campaign_type} campaign for {segment} looks viable. Monitor early results and optimize."
    elif roi > 0:
        return f"Marginal positive ROI. Consider A/B testing before full rollout to {segment}."
    else:
        return f"Negative ROI projected for {segment} with {campaign_type}. Consider alternative channels or stronger offers."

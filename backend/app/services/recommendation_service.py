"""
Campaign recommendations by segment.
"""

RECOMMENDATIONS = {
    "VIP Customers": {
        "segment": "VIP Customers",
        "description": "Top-tier customers with high recency, frequency, and monetary value. They are the most valuable segment.",
        "campaigns": [
            {"type": "Loyalty Program", "objective": "Retain and reward", "message": "Exclusive VIP access to new collections and priority support.", "priority": "High"},
            {"type": "Early Access", "objective": "Increase engagement", "message": "Be the first to shop our new arrivals — VIP-only preview.", "priority": "High"},
            {"type": "Premium Offers", "objective": "Increase AOV", "message": "Curated premium bundles selected just for you.", "priority": "Medium"},
        ],
        "business_goal": "Maximize retention and lifetime value of the most profitable customers.",
    },
    "Loyal Customers": {
        "segment": "Loyal Customers",
        "description": "Frequent buyers with recent activity and good spending. Reliable repeat purchasers.",
        "campaigns": [
            {"type": "Referral Program", "objective": "Acquisition via advocacy", "message": "Share the love — give £10, get £10 for every friend who joins.", "priority": "High"},
            {"type": "Cross-Sell", "objective": "Expand basket", "message": "Customers like you also loved these products.", "priority": "Medium"},
            {"type": "Birthday Rewards", "objective": "Build emotional connection", "message": "A special gift for your special day.", "priority": "Low"},
        ],
        "business_goal": "Nurture loyalty and turn them into VIP customers through upselling.",
    },
    "New Customers": {
        "segment": "New Customers",
        "description": "Recently acquired customers with few purchases. High potential for conversion to loyal buyers.",
        "campaigns": [
            {"type": "Onboarding Series", "objective": "Educate and engage", "message": "Welcome! Here's how to get the most out of your account.", "priority": "High"},
            {"type": "Product Recommendations", "objective": "Drive second purchase", "message": "Based on your first order, you might love these.", "priority": "High"},
            {"type": "Welcome Discount", "objective": "Encourage repeat purchase", "message": "15% off your next order — welcome to the family!", "priority": "Medium"},
        ],
        "business_goal": "Convert one-time buyers into repeat customers within 30 days.",
    },
    "At-Risk Customers": {
        "segment": "At-Risk Customers",
        "description": "Previously active customers who haven't purchased recently. High historical value but fading engagement.",
        "campaigns": [
            {"type": "Reactivation Email", "objective": "Re-engage", "message": "We miss you! Here's 20% off to welcome you back.", "priority": "Critical"},
            {"type": "Win-Back Survey", "objective": "Understand churn drivers", "message": "We'd love your feedback — what can we do better?", "priority": "High"},
            {"type": "Personalized Offer", "objective": "Trigger purchase", "message": "Your favorite items are back in stock with a special price.", "priority": "High"},
        ],
        "business_goal": "Prevent churn and reactivate high-value customers before they become lost.",
    },
    "Lost Customers": {
        "segment": "Lost Customers",
        "description": "Customers with very low recency, frequency, and monetary value. Likely churned.",
        "campaigns": [
            {"type": "Win-Back Campaign", "objective": "Last attempt to recover", "message": "It's been a while — here's 30% off to come back.", "priority": "Medium"},
            {"type": "Strong Incentive", "objective": "Break inertia", "message": "Free shipping + 25% off — just for you.", "priority": "Medium"},
            {"type": "Exit Survey", "objective": "Learn from churn", "message": "We'd love to know what happened. Quick 2-min survey.", "priority": "Low"},
        ],
        "business_goal": "Attempt recovery with strong incentives; gather insights for prevention.",
    },
    "Occasional Buyers": {
        "segment": "Occasional Buyers",
        "description": "Moderate engagement customers who buy sporadically. Potential to increase frequency.",
        "campaigns": [
            {"type": "Frequency Boost", "objective": "Increase purchase cadence", "message": "Shop this week and earn double reward points!", "priority": "Medium"},
            {"type": "Bundle Offers", "objective": "Increase AOV", "message": "Save 20% when you buy 3+ items.", "priority": "Medium"},
            {"type": "Seasonal Campaign", "objective": "Timely relevance", "message": "Spring essentials picked just for you.", "priority": "Low"},
        ],
        "business_goal": "Increase purchase frequency and convert to loyal/regular segment.",
    },
    "High Potential": {
        "segment": "High Potential",
        "description": "Good recency and spending but room to grow in frequency. Strong upselling candidates.",
        "campaigns": [
            {"type": "Cross-Selling", "objective": "Expand product range", "message": "Complete your collection — items that pair perfectly.", "priority": "High"},
            {"type": "Up-Selling", "objective": "Increase order value", "message": "Upgrade to premium for just £5 more.", "priority": "High"},
            {"type": "Personalized Bundles", "objective": "Drive larger baskets", "message": "Your custom bundle — 3 items, 1 great price.", "priority": "Medium"},
        ],
        "business_goal": "Maximize value extraction through cross-sell and up-sell strategies.",
    },
}


def get_all_recommendations() -> list:
    return list(RECOMMENDATIONS.values())


def get_recommendation_for_segment(segment: str) -> dict:
    return RECOMMENDATIONS.get(segment)

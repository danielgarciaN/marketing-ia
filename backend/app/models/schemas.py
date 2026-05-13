"""API schemas."""
from pydantic import BaseModel
from typing import Optional


class CampaignSimulationRequest(BaseModel):
    segment: str
    campaign_type: str = "email"
    budget: float = 1000.0
    discount_pct: float = 10.0
    expected_conversion_rate: float = 5.0

"""Campaign endpoints."""
from fastapi import APIRouter
from app.models.schemas import CampaignSimulationRequest
from app.services.recommendation_service import get_all_recommendations
from app.services.campaign_simulator_service import simulate_campaign

router = APIRouter(prefix="/campaigns", tags=["Campaigns"])


@router.get("/recommendations")
def get_recommendations():
    return get_all_recommendations()


@router.post("/simulate")
def run_simulation(req: CampaignSimulationRequest):
    return simulate_campaign(
        segment=req.segment,
        campaign_type=req.campaign_type,
        budget=req.budget,
        discount_pct=req.discount_pct,
        expected_conversion_rate=req.expected_conversion_rate,
    )

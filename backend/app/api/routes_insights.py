"""Insight endpoints."""
from fastapi import APIRouter
from app.services.insight_service import generate_insights
from app.services.data_service import data_service

router = APIRouter(prefix="/insights", tags=["Insights"])


@router.get("")
def get_insights():
    return generate_insights()


@router.get("/model-metrics")
def get_model_metrics():
    data_service.load()
    return data_service.model_metrics


@router.get("/clusters")
def get_clusters():
    data_service.load()
    return data_service.cluster_interpretations

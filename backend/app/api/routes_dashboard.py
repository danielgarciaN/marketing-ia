"""Dashboard endpoints."""
from fastapi import APIRouter
from app.services.data_service import data_service

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/summary")
def get_summary():
    data_service.load()
    return data_service.dashboard_summary


@router.get("/revenue")
def get_revenue():
    data_service.load()
    return data_service.revenue_monthly

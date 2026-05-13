"""Segment endpoints."""
from fastapi import APIRouter, HTTPException
from app.services.data_service import data_service
from app.services.recommendation_service import get_recommendation_for_segment

router = APIRouter(prefix="/segments", tags=["Segments"])


@router.get("")
def get_segments():
    data_service.load()
    segments = data_service.segment_summary
    for s in segments:
        rec = get_recommendation_for_segment(s["segment"])
        s["description"] = rec["description"] if rec else ""
        s["business_goal"] = rec["business_goal"] if rec else ""
    return segments


@router.get("/{segment_name}")
def get_segment(segment_name: str):
    data_service.load()
    seg = next((s for s in data_service.segment_summary if s["segment"] == segment_name), None)
    if not seg:
        raise HTTPException(status_code=404, detail="Segment not found")

    rec = get_recommendation_for_segment(segment_name)
    customers = data_service.get_customers_by_segment(segment_name)

    return {
        **seg,
        "description": rec["description"] if rec else "",
        "business_goal": rec["business_goal"] if rec else "",
        "campaigns": rec["campaigns"] if rec else [],
        "customers": customers[:100],  # limit
    }

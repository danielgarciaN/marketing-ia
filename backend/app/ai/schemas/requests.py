"""Request schemas for the AI layer endpoints."""
from typing import Literal
from pydantic import BaseModel, Field


class AIQueryRequest(BaseModel):
    query: str = Field(..., min_length=3, max_length=2000, description="Natural language question")
    session_id: str | None = Field(None, description="Continue an existing conversation")
    stream: bool = Field(False, description="Enable SSE streaming (future)")

    model_config = {"json_schema_extra": {
        "example": {
            "query": "¿Qué segmento deberíamos priorizar este mes y qué campaña lanzar?",
            "session_id": None,
            "stream": False,
        }
    }}


class AIReportRequest(BaseModel):
    report_type: Literal["executive", "segment", "campaign", "forecast"] = "executive"
    segment: str | None = Field(None, description="Restrict to a specific segment")
    include_forecast: bool = True
    include_recommendations: bool = True
    language: Literal["es", "en"] = "es"


class AIRecommendationRequest(BaseModel):
    segment: str | None = None
    budget: float | None = Field(None, gt=0)
    objective: Literal["revenue", "retention", "acquisition", "reactivation"] = "revenue"
    top_n: int = Field(3, ge=1, le=10)

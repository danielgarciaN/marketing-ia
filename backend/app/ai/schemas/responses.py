"""Response schemas for the AI layer endpoints."""
from typing import Any
from pydantic import BaseModel, Field


class TraceStep(BaseModel):
    agent: str
    action: str
    tools_called: list[str] = []
    duration_ms: float = 0.0


class AIQueryResponse(BaseModel):
    session_id: str
    query: str
    intent: str
    response: str
    agents_used: list[str]
    tools_used: list[str]
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    retrieved_docs_count: int = 0
    execution_trace: list[TraceStep] = []
    analysis_results: dict[str, Any] = {}
    recommendations: list[dict[str, Any]] = []
    forecast_data: dict[str, Any] = {}

    model_config = {"json_schema_extra": {
        "example": {
            "session_id": "sess_abc123",
            "query": "¿Qué segmento priorizar?",
            "intent": "campaign",
            "response": "Recomendamos priorizar el segmento **At-Risk** con una campaña de win-back...",
            "agents_used": ["supervisor", "data_analyst", "campaign_strategy", "insight_narrator"],
            "tools_used": ["get_segment_overview", "simulate_campaign", "retrieve_marketing_knowledge"],
            "confidence_score": 0.92,
            "retrieved_docs_count": 4,
            "execution_trace": [],
        }
    }}


class AITraceResponse(BaseModel):
    session_id: str
    total_agents: int
    total_tools: int
    total_iterations: int
    steps: list[TraceStep]


class AIReportResponse(BaseModel):
    report_type: str
    title: str
    executive_summary: str
    sections: list[dict[str, Any]]
    generated_at: str
    agents_used: list[str]


class AIHealthResponse(BaseModel):
    status: str
    llm_available: bool
    rag_available: bool
    agents: list[str]
    version: str = "2.0.0"

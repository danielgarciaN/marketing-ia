"""FastAPI routes for the AI multiagent layer."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from app.ai.memory.conversation import memory_store
from app.ai.schemas.requests import AIQueryRequest, AIRecommendationRequest, AIReportRequest
from app.ai.schemas.responses import AIHealthResponse, AIQueryResponse, AIReportResponse, AITraceResponse, TraceStep
from app.ai.services.ai_service import ai_service

router = APIRouter(prefix="/ai", tags=["AI Multiagent"])


# ── Health ────────────────────────────────────────────────────────────────────

@router.get("/health", response_model=AIHealthResponse, summary="AI layer health check")
async def ai_health() -> AIHealthResponse:
    """Check availability of LLM, RAG, and agents."""
    from app.ai.config import get_ai_settings
    cfg = get_ai_settings()
    llm_available = bool(cfg.openai_api_key)

    rag_ok = False
    try:
        from app.ai.rag.store import get_vector_store
        get_vector_store()
        rag_ok = True
    except Exception:
        pass

    return AIHealthResponse(
        status="ok" if llm_available else "degraded",
        llm_available=llm_available,
        rag_available=rag_ok,
        agents=[
            "supervisor", "data_analyst", "sql_pandas",
            "rag_knowledge", "campaign_strategy", "forecasting", "insight_narrator",
        ],
    )


# ── Core query ────────────────────────────────────────────────────────────────

@router.post("/query", response_model=AIQueryResponse, summary="Natural language query")
async def ai_query(request: AIQueryRequest) -> AIQueryResponse:
    """Submit a natural language question to the multiagent system.

    The supervisor classifies the intent and orchestrates the appropriate
    chain of specialised agents to produce a business-grade response.
    """
    try:
        return await ai_service.process_query(request.query, request.session_id)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Agent execution failed: {exc}",
        ) from exc


# ── Conversations ─────────────────────────────────────────────────────────────

@router.get("/conversations/{session_id}", summary="Retrieve conversation history")
async def get_conversation(session_id: str) -> dict:
    """Return the full conversation history for a session."""
    if not memory_store.session_exists(session_id):
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found.")
    history = memory_store.get_history(session_id)
    return {
        "session_id": session_id,
        "turn_count": len(history),
        "history": [
            {"role": t.role, "content": t.content, "timestamp": t.timestamp}
            for t in history
        ],
    }


@router.delete("/conversations/{session_id}", summary="Clear a conversation session")
async def clear_conversation(session_id: str) -> dict:
    memory_store.clear_session(session_id)
    return {"status": "cleared", "session_id": session_id}


# ── Traces ────────────────────────────────────────────────────────────────────

@router.get("/traces/{session_id}", response_model=AITraceResponse, summary="Get execution trace")
async def get_trace(session_id: str) -> AITraceResponse:
    """Return the execution trace for the last query in a session.

    Note: Traces are embedded in the query response. This endpoint
    reconstructs a summary from conversation metadata.
    """
    if not memory_store.session_exists(session_id):
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found.")

    history = memory_store.get_history(session_id)
    agents: list[str] = []
    for turn in history:
        if turn.role == "assistant":
            agents.extend(turn.metadata.get("agents_used", []))

    return AITraceResponse(
        session_id=session_id,
        total_agents=len(set(agents)),
        total_tools=0,
        total_iterations=len([t for t in history if t.role == "user"]),
        steps=[TraceStep(agent=a, action="executed", tools_called=[]) for a in dict.fromkeys(agents)],
    )


# ── Reports ───────────────────────────────────────────────────────────────────

@router.post("/report", response_model=AIReportResponse, summary="Generate AI report")
async def generate_report(request: AIReportRequest) -> AIReportResponse:
    """Generate a structured AI-powered business report.

    Report types: executive | segment | campaign | forecast
    """
    try:
        return await ai_service.generate_report(
            report_type=request.report_type,
            segment=request.segment,
            language=request.language,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


# ── Recommendations ───────────────────────────────────────────────────────────

@router.post("/recommendations", response_model=AIQueryResponse, summary="AI campaign recommendations")
async def ai_recommendations(request: AIRecommendationRequest) -> AIQueryResponse:
    """Use the multiagent system to generate and rank campaign recommendations.

    Orchestrates: data_analyst → campaign_strategy → insight_narrator
    """
    segment_ctx = f" para el segmento '{request.segment}'" if request.segment else ""
    budget_ctx = f" con presupuesto de {request.budget}" if request.budget else ""
    query = (
        f"Recomienda las {request.top_n} mejores campañas{segment_ctx}{budget_ctx} "
        f"con objetivo de {request.objective}. Incluye ROI estimado y priorización."
    )
    try:
        return await ai_service.process_query(query)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


# ── RAG Ingestion ─────────────────────────────────────────────────────────────

@router.post("/rag/ingest", summary="Ingest documents into the knowledge base")
async def ingest_documents() -> dict:
    """Trigger document ingestion from the default docs/ directory into Qdrant.

    Supports PDF, Markdown, and plain text files.
    """
    try:
        from app.ai.rag.ingestion import ingest_directory
        result = ingest_directory()
        return {"status": "success", **result}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

"""AI Service — orchestrates the LangGraph pipeline and maps state to API responses."""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any

from app.ai.graph.executor import run_graph
from app.ai.graph.state import AgentState
from app.ai.memory.conversation import memory_store
from app.ai.schemas.responses import AIQueryResponse, AIReportResponse, TraceStep


class AIService:
    """Application-level service that bridges FastAPI routes and the LangGraph engine."""

    async def process_query(self, query: str, session_id: str | None = None) -> AIQueryResponse:
        """Run the full multiagent graph for a natural language query."""
        session_id = session_id or str(uuid.uuid4())

        # Prepend conversation context if session exists
        enriched_query = query
        if memory_store.session_exists(session_id):
            ctx = memory_store.get_context_window(session_id, last_n=4)
            enriched_query = f"[Conversation context]\n{ctx}\n\n[New question]\n{query}"

        final_state: AgentState = await run_graph(enriched_query, session_id)

        # Persist turn in memory
        memory_store.add_turn(session_id, "user", query)
        if final_state.get("final_response"):
            memory_store.add_turn(
                session_id,
                "assistant",
                final_state["final_response"],
                metadata={"agents_used": final_state.get("agents_used", [])},
            )

        trace_steps = [
            TraceStep(
                agent=s["agent"],
                action=s["action"],
                tools_called=s.get("tools_called", []),
                duration_ms=s.get("duration_ms", 0.0),
            )
            for s in final_state.get("execution_trace", [])
        ]

        return AIQueryResponse(
            session_id=session_id,
            query=query,
            intent=final_state.get("intent", "general"),
            response=final_state.get("final_response", "No response generated."),
            agents_used=final_state.get("agents_used", []),
            tools_used=final_state.get("tools_used", []),
            confidence_score=final_state.get("confidence_score", 0.0),
            retrieved_docs_count=len(final_state.get("retrieved_docs", [])),
            execution_trace=trace_steps,
            analysis_results=final_state.get("analysis_results", {}),
            recommendations=final_state.get("recommendations", []),
            forecast_data=final_state.get("forecast_data", {}),
        )

    async def generate_report(
        self,
        report_type: str = "executive",
        segment: str | None = None,
        language: str = "es",
    ) -> AIReportResponse:
        """Generate a structured AI report by running a targeted graph query."""
        query_map = {
            "executive": "Genera un resumen ejecutivo completo del estado actual del negocio con KPIs, tendencias y recomendaciones de campaña.",
            "segment": f"Analiza en detalle el segmento {segment or 'todos'} con estadísticas, riesgo de churn y recomendaciones de campaña.",
            "campaign": "Evalúa todas las oportunidades de campaña disponibles, simula ROI y recomienda las 3 mejores opciones.",
            "forecast": "Genera previsión de revenue para los próximos 3 meses, estima riesgo de churn y calcula LTV por segmento.",
        }
        query = query_map.get(report_type, query_map["executive"])
        result = await self.process_query(query)

        return AIReportResponse(
            report_type=report_type,
            title=f"AI Marketing Report — {report_type.title()}",
            executive_summary=result.response,
            sections=[
                {"title": "Analysis", "content": result.analysis_results},
                {"title": "Recommendations", "content": result.recommendations},
                {"title": "Forecast", "content": result.forecast_data},
            ],
            generated_at=datetime.now(timezone.utc).isoformat(),
            agents_used=result.agents_used,
        )


# Singleton
ai_service = AIService()

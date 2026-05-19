"""Graph execution engine — initialises state and runs the LangGraph workflow."""
from __future__ import annotations

import uuid
from typing import Any

from langchain_core.messages import HumanMessage

from app.ai.config import get_ai_settings
from app.ai.graph.builder import get_compiled_graph
from app.ai.graph.state import AgentState


def _initial_state(query: str, session_id: str) -> AgentState:
    """Build the initial AgentState for a new query."""
    return AgentState(
        messages=[HumanMessage(content=query)],
        session_id=session_id,
        user_query=query,
        intent="general",
        active_agent="supervisor",
        next_agent="supervisor",
        agents_used=[],
        tools_used=[],
        iteration_count=0,
        execution_trace=[],
        retrieved_docs=[],
        analysis_results={},
        recommendations=[],
        forecast_data={},
        final_response="",
        confidence_score=0.0,
        error=None,
    )


async def run_graph(query: str, session_id: str | None = None) -> AgentState:
    """Execute the multiagent graph for a user query.

    Args:
        query: Natural language question from the user.
        session_id: Optional session identifier for continuity.

    Returns:
        Final AgentState with populated final_response, agents_used, etc.
    """
    cfg = get_ai_settings()
    session_id = session_id or str(uuid.uuid4())
    graph = get_compiled_graph()

    initial_state = _initial_state(query, session_id)

    config = {
        "recursion_limit": cfg.recursion_limit,
        "configurable": {"session_id": session_id},
    }

    try:
        final_state: AgentState = await graph.ainvoke(initial_state, config=config)
    except Exception as exc:
        initial_state["error"] = str(exc)
        initial_state["final_response"] = (
            f"Lo siento, ocurrió un error durante el análisis: {exc}"
        )
        return initial_state

    return final_state


def run_graph_sync(query: str, session_id: str | None = None) -> AgentState:
    """Synchronous wrapper for run_graph — use in non-async contexts."""
    import asyncio
    return asyncio.run(run_graph(query, session_id))

"""Conditional edge routing logic for the LangGraph state machine."""
from __future__ import annotations

from app.ai.graph.state import AgentState


def route_from_supervisor(state: AgentState) -> str:
    """Determine which node to execute after the supervisor decision.

    The supervisor sets `next_agent` in state via Command(goto=...).
    This function is used as a fallback router for conditional edges
    when explicit Command routing is not sufficient.
    """
    next_agent = state.get("next_agent", "data_analyst")
    iteration = state.get("iteration_count", 0)
    max_iter = 12

    # Safety: force narrative generation if too many iterations
    if iteration >= max_iter:
        return "insight_narrator"

    valid_agents = {
        "data_analyst",
        "sql_pandas",
        "rag_knowledge",
        "campaign_strategy",
        "forecasting",
        "insight_narrator",
        "__end__",
    }

    return next_agent if next_agent in valid_agents else "data_analyst"


def should_continue_or_end(state: AgentState) -> str:
    """After insight_narrator runs, always go to END."""
    agents_used = state.get("agents_used", [])
    if "insight_narrator" in agents_used and state.get("final_response"):
        return "__end__"
    return "supervisor"

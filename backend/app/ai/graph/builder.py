"""LangGraph graph construction — assembles all agents into a runnable state machine."""
from __future__ import annotations

from functools import lru_cache

from langgraph.graph import END, START, StateGraph

from app.ai.agents.campaign_strategy import campaign_strategy_node
from app.ai.agents.data_analyst import data_analyst_node
from app.ai.agents.forecasting import forecasting_node
from app.ai.agents.insight_narrator import insight_narrator_node
from app.ai.agents.rag_knowledge import rag_knowledge_node
from app.ai.agents.sql_pandas import sql_pandas_node
from app.ai.agents.supervisor import supervisor_node
from app.ai.graph.state import AgentState


def build_graph():
    """Build and compile the multiagent LangGraph state machine.

    Topology (Command-driven routing):
        START → supervisor ─(Command)─► worker ─(Command)─► supervisor ─► ... ─► END

    All routing is handled via Command(goto=...) returned by each node.
    No conditional_edges needed — LangGraph 1.x resolves targets at runtime.
    """
    graph = StateGraph(AgentState)

    # ── Register all nodes ────────────────────────────────────────────────────
    graph.add_node("supervisor", supervisor_node)
    graph.add_node("data_analyst", data_analyst_node)
    graph.add_node("sql_pandas", sql_pandas_node)
    graph.add_node("rag_knowledge", rag_knowledge_node)
    graph.add_node("campaign_strategy", campaign_strategy_node)
    graph.add_node("forecasting", forecasting_node)
    graph.add_node("insight_narrator", insight_narrator_node)

    # ── Entry point ───────────────────────────────────────────────────────────
    graph.add_edge(START, "supervisor")

    # ── Terminal edge ─────────────────────────────────────────────────────────
    # insight_narrator always returns Command(goto="__end__") but we declare
    # the edge so the graph compiler knows this path terminates.
    graph.add_edge("insight_narrator", END)

    # All other routing is handled by Command(goto=...) inside each node.
    # supervisor  → Command(goto=<worker> | "__end__")
    # workers     → Command(goto="supervisor")

    return graph.compile()


@lru_cache(maxsize=1)
def get_compiled_graph():
    """Return the singleton compiled graph (thread-safe after first call)."""
    return build_graph()

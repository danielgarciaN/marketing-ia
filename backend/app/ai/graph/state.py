"""Shared LangGraph state — single source of truth across all agents."""
from __future__ import annotations

from typing import Annotated, Any, Literal
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict

# Intent taxonomy understood by the Supervisor
Intent = Literal[
    "analytics",       # KPI, revenue, trends, customer behaviour
    "segmentation",    # Segment analysis, RFM distribution
    "campaign",        # Campaign recommendations and simulation
    "forecast",        # Revenue / churn prediction
    "knowledge",       # RAG-backed marketing best practices
    "report",          # Executive narrative summary
    "general",         # Falls back to data analyst
]

AgentName = Literal[
    "supervisor",
    "data_analyst",
    "sql_pandas",
    "rag_knowledge",
    "campaign_strategy",
    "forecasting",
    "insight_narrator",
    "__end__",
]


class ExecutionStep(TypedDict):
    agent: str
    action: str
    input_summary: str
    output_summary: str
    duration_ms: float
    tools_called: list[str]


class AgentState(TypedDict):
    # ── Conversation ──────────────────────────────────────────────────────────
    messages: Annotated[list[BaseMessage], add_messages]
    session_id: str
    user_query: str

    # ── Routing ───────────────────────────────────────────────────────────────
    intent: Intent
    active_agent: AgentName
    next_agent: AgentName

    # ── Execution bookkeeping ─────────────────────────────────────────────────
    agents_used: list[str]
    tools_used: list[str]
    iteration_count: int
    execution_trace: list[ExecutionStep]

    # ── Data payloads ─────────────────────────────────────────────────────────
    retrieved_docs: list[dict[str, Any]]
    analysis_results: dict[str, Any]
    recommendations: list[dict[str, Any]]
    forecast_data: dict[str, Any]

    # ── Output ────────────────────────────────────────────────────────────────
    final_response: str
    confidence_score: float       # 0.0 – 1.0
    error: str | None

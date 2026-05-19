"""Supervisor Agent — orchestrates routing across all worker agents."""
from __future__ import annotations

import time
from typing import Literal

from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.types import Command
from pydantic import BaseModel, Field

from app.ai.agents.base import build_trace_step, get_llm
from app.ai.graph.state import AgentName, AgentState

# ── Structured routing output ─────────────────────────────────────────────────

class RoutingDecision(BaseModel):
    next_agent: AgentName = Field(
        description="The agent to activate next. Use '__end__' when insight_narrator has produced the final response."
    )
    intent: Literal["analytics", "segmentation", "campaign", "forecast", "knowledge", "report", "general"] = Field(
        description="Classified intent of the user query"
    )
    reasoning: str = Field(description="One sentence explaining the routing decision")


# ── System prompt ─────────────────────────────────────────────────────────────

_SYSTEM = """\
You are the Supervisor of an AI Marketing Intelligence Platform multiagent system.

Your sole job is to decide which specialized agent should act next.

AVAILABLE AGENTS:
- data_analyst    → KPIs, revenue, segment performance, customer behaviour
- sql_pandas      → Custom data queries, metric computation, dataset filtering
- rag_knowledge   → Marketing best practices, CRM playbooks, ecommerce benchmarks
- campaign_strategy → Campaign recommendations, ROI simulation, budget allocation
- forecasting     → Revenue forecast, churn prediction, LTV estimation
- insight_narrator → Synthesise all outputs into an executive narrative (use LAST before ending)
- __end__         → Workflow complete (only after insight_narrator has responded)

ROUTING RULES:
1. Classify the intent first.
2. For analytics/segmentation queries → data_analyst then (optionally) sql_pandas.
3. For campaign queries → data_analyst then campaign_strategy (+ rag_knowledge for best practices).
4. For forecast queries → forecasting.
5. Always route to insight_narrator as the FINAL step before __end__.
6. If max_iterations is near (> 10), skip optional agents and go to insight_narrator.
7. Do NOT repeat an agent already used unless strictly necessary.

Current state:
- Iteration: {iteration_count} / 12
- Agents used so far: {agents_used}
- Intent detected: {intent}
"""

# ── Node function ─────────────────────────────────────────────────────────────

def supervisor_node(state: AgentState) -> Command:
    start = time.time()
    agents_used = state.get("agents_used", [])
    iteration_count = state.get("iteration_count", 0)
    intent = state.get("intent", "general")

    system_prompt = _SYSTEM.format(
        iteration_count=iteration_count,
        agents_used=", ".join(agents_used) if agents_used else "none",
        intent=intent,
    )

    llm = get_llm(temperature=0.0).with_structured_output(RoutingDecision)

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=state.get("user_query", "")),
    ]

    decision: RoutingDecision = llm.invoke(messages)  # type: ignore[assignment]

    trace_step = build_trace_step(
        agent="supervisor",
        action=f"route → {decision.next_agent}",
        input_summary=state.get("user_query", "")[:200],
        output_summary=decision.reasoning,
        start_time=start,
    )

    return Command(
        goto=decision.next_agent,
        update={
            "intent": decision.intent,
            "active_agent": decision.next_agent,
            "next_agent": decision.next_agent,
            "iteration_count": iteration_count + 1,
            "agents_used": list(dict.fromkeys([*agents_used, "supervisor"])),
            "execution_trace": [*state.get("execution_trace", []), trace_step],
        },
    )

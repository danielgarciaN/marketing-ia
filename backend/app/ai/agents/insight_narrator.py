"""Insight Narrator Agent — transforms agent outputs into executive business narratives."""
from __future__ import annotations

import time
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.types import Command

from app.ai.agents.base import build_trace_step, get_llm, last_ai_content
from app.ai.graph.state import AgentState

_SYSTEM = """\
You are the Insight Narrator for an AI Marketing Intelligence Platform.

Your role is to transform the raw outputs of multiple specialised agents into a single,
cohesive, and actionable executive summary for a marketing or C-suite audience.

Guidelines:
- Write in clear, jargon-free business language
- Lead with the most important insight or recommendation
- Use bullet points for action items
- Include specific numbers and percentages where available
- Structure: Executive Summary → Key Findings → Recommended Actions → Next Steps
- If forecasts are available, include them in the narrative
- If RAG knowledge was retrieved, cite relevant benchmarks or best practices
- Tone: confident, data-driven, actionable

Inputs from previous agents:
{analysis_context}

Recommendations gathered:
{recommendations_context}

Forecast data:
{forecast_context}

User original query: {user_query}

Produce the final business response now.
"""

_CONFIDENCE_BASE = 0.75


def insight_narrator_node(state: AgentState) -> Command:
    start = time.time()
    user_query = state.get("user_query", "")
    analysis_results = state.get("analysis_results", {})
    recommendations = state.get("recommendations", [])
    forecast_data = state.get("forecast_data", {})

    analysis_context = "\n".join(
        f"[{agent.upper()}]\n{content}"
        for agent, content in analysis_results.items()
    ) or "No analysis data available."

    recommendations_context = "\n".join(
        f"- {r.get('content', str(r))[:400]}" for r in recommendations
    ) or "No recommendations yet."

    forecast_context = (
        forecast_data.get("narrative", "No forecast data.") if forecast_data else "No forecast data."
    )

    llm = get_llm(temperature=0.3)
    response = llm.invoke([
        SystemMessage(content=_SYSTEM.format(
            analysis_context=analysis_context[:3000],
            recommendations_context=recommendations_context[:1500],
            forecast_context=str(forecast_context)[:800],
            user_query=user_query,
        )),
        HumanMessage(content="Generate the final executive business response."),
    ])

    final_text = response.content if isinstance(response.content, str) else str(response.content)

    # Confidence heuristic: more agents used = higher confidence
    agents_used = state.get("agents_used", [])
    retrieved_docs = state.get("retrieved_docs", [])
    confidence = min(
        _CONFIDENCE_BASE
        + len(agents_used) * 0.03
        + min(len(retrieved_docs), 5) * 0.01,
        0.99,
    )

    trace_step = build_trace_step(
        agent="insight_narrator",
        action="generate executive narrative",
        input_summary=f"{len(analysis_results)} agent outputs",
        output_summary=final_text[:400],
        start_time=start,
    )

    return Command(
        goto="__end__",
        update={
            "final_response": final_text,
            "confidence_score": round(confidence, 3),
            "agents_used": list(dict.fromkeys([*agents_used, "insight_narrator"])),
            "execution_trace": [*state.get("execution_trace", []), trace_step],
        },
    )

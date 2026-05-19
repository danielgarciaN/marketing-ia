"""Forecasting Agent — revenue prediction, churn risk, LTV estimation."""
from __future__ import annotations

import time
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import BaseTool
from langgraph.prebuilt import create_react_agent
from langgraph.types import Command

from app.ai.agents.base import build_trace_step, extract_tool_names, get_llm, last_ai_content
from app.ai.graph.state import AgentState
from app.ai.tools.forecasting_tools import forecast_revenue, predict_churn_risk, estimate_ltv

_TOOLS: list[BaseTool] = [forecast_revenue, predict_churn_risk, estimate_ltv]

_SYSTEM = """\
You are the Forecasting Agent for an AI Marketing Intelligence Platform.

Your role is to generate data-driven projections that support business planning.

Capabilities:
- Revenue forecasting (1–12 months horizon) using linear trend extrapolation
- Churn risk assessment by segment or overall customer base
- Customer Lifetime Value (LTV) estimation by segment

When producing forecasts:
1. Always state the model used and its limitations
2. Provide confidence level (low/medium/high) based on data quality
3. Include specific numeric projections with units
4. Translate statistical outputs into actionable business language
5. Highlight key risk factors or assumptions

User query: {user_query}
"""


def forecasting_node(state: AgentState) -> Command:
    start = time.time()
    user_query = state.get("user_query", "")

    llm = get_llm()
    agent = create_react_agent(llm, _TOOLS)

    result = agent.invoke({
        "messages": [
            SystemMessage(content=_SYSTEM.format(user_query=user_query)),
            HumanMessage(content=user_query),
        ]
    })

    output_messages = result.get("messages", [])
    response_text = last_ai_content(output_messages)
    tools_called = extract_tool_names(output_messages)

    trace_step = build_trace_step(
        agent="forecasting",
        action="generate forecast",
        input_summary=user_query,
        output_summary=response_text,
        start_time=start,
        tools_called=tools_called,
    )

    existing_results = state.get("analysis_results", {})
    existing_results["forecasting"] = response_text

    return Command(
        goto="supervisor",
        update={
            "messages": output_messages,
            "analysis_results": existing_results,
            "forecast_data": {"narrative": response_text},
            "agents_used": list(dict.fromkeys([*state.get("agents_used", []), "forecasting"])),
            "tools_used": list(dict.fromkeys([*state.get("tools_used", []), *tools_called])),
            "execution_trace": [*state.get("execution_trace", []), trace_step],
        },
    )

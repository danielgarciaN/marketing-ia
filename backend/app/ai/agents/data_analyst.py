"""Data Analyst Agent — KPI analysis, segment performance, revenue trends."""
from __future__ import annotations

import time
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import BaseTool
from langgraph.prebuilt import create_react_agent
from langgraph.types import Command

from app.ai.agents.base import build_trace_step, extract_tool_names, get_llm, last_ai_content
from app.ai.graph.state import AgentState
from app.ai.tools.data_tools import get_dashboard_summary, get_segment_overview, get_customers_by_segment
from app.ai.tools.analytics_tools import compute_segment_stats, get_rfm_distribution, get_revenue_trend

_TOOLS: list[BaseTool] = [
    get_dashboard_summary,
    get_segment_overview,
    get_customers_by_segment,
    compute_segment_stats,
    get_rfm_distribution,
    get_revenue_trend,
]

_SYSTEM = """\
You are the Data Analyst Agent for an ecommerce marketing intelligence platform.

Your capabilities:
- Retrieve and analyse KPI summaries (revenue, orders, customer counts)
- Inspect RFM segment performance (size, revenue share, recency, frequency, monetary)
- Compute detailed statistics for any customer segment
- Identify trends in revenue over time
- Compare segment performance to find opportunities and risks

When analysing, always:
1. Retrieve the relevant data using tools
2. Provide specific numbers and percentages
3. Flag anomalies or concerning trends
4. Structure your output as clear business insights

User query: {user_query}
"""


def data_analyst_node(state: AgentState) -> Command:
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
        agent="data_analyst",
        action="analyse data",
        input_summary=user_query,
        output_summary=response_text,
        start_time=start,
        tools_called=tools_called,
    )

    existing_results = state.get("analysis_results", {})
    existing_results["data_analyst"] = response_text

    return Command(
        goto="supervisor",
        update={
            "messages": output_messages,
            "analysis_results": existing_results,
            "agents_used": list(dict.fromkeys([*state.get("agents_used", []), "data_analyst"])),
            "tools_used": list(dict.fromkeys([*state.get("tools_used", []), *tools_called])),
            "execution_trace": [*state.get("execution_trace", []), trace_step],
        },
    )

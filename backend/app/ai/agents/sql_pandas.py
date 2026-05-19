"""SQL/Pandas Agent — dynamic queries, metric computation, dataset filtering."""
from __future__ import annotations

import time
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import BaseTool
from langgraph.prebuilt import create_react_agent
from langgraph.types import Command

from app.ai.agents.base import build_trace_step, extract_tool_names, get_llm, last_ai_content
from app.ai.graph.state import AgentState
from app.ai.tools.analytics_tools import run_pandas_query, compute_segment_stats, get_rfm_distribution
from app.ai.tools.data_tools import get_customers_by_segment, get_customer_by_id

_TOOLS: list[BaseTool] = [
    run_pandas_query,
    compute_segment_stats,
    get_rfm_distribution,
    get_customers_by_segment,
    get_customer_by_id,
]

_SYSTEM = """\
You are the SQL/Pandas Agent for an ecommerce analytics platform.

Your capabilities:
- Execute Pandas query expressions against the customer dataset
- Filter customers by any combination of RFM scores, segment, cluster, spend, recency
- Compute aggregated metrics (mean, median, count, sum, percentile) for any slice of data
- Retrieve individual customer profiles for deep-dive analysis

Pandas query syntax examples:
- "Monetary > 500 and Recency < 30"
- "Segment == 'VIP Customers' and F_Score >= 4"
- "R_Score <= 2 and Frequency > 10"

Always report:
- The filter applied
- Row count returned
- Key statistics of the result set
- Business interpretation

User query: {user_query}
"""


def sql_pandas_node(state: AgentState) -> Command:
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
        agent="sql_pandas",
        action="query data",
        input_summary=user_query,
        output_summary=response_text,
        start_time=start,
        tools_called=tools_called,
    )

    existing_results = state.get("analysis_results", {})
    existing_results["sql_pandas"] = response_text

    return Command(
        goto="supervisor",
        update={
            "messages": output_messages,
            "analysis_results": existing_results,
            "agents_used": list(dict.fromkeys([*state.get("agents_used", []), "sql_pandas"])),
            "tools_used": list(dict.fromkeys([*state.get("tools_used", []), *tools_called])),
            "execution_trace": [*state.get("execution_trace", []), trace_step],
        },
    )

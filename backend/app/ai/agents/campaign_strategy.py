"""Campaign Strategy Agent — recommends, simulates and prioritises campaigns."""
from __future__ import annotations

import time
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import BaseTool
from langgraph.prebuilt import create_react_agent
from langgraph.types import Command

from app.ai.agents.base import build_trace_step, extract_tool_names, get_llm, last_ai_content
from app.ai.graph.state import AgentState
from app.ai.tools.campaign_tools import get_campaign_recommendations, simulate_campaign, rank_segments_by_opportunity

_TOOLS: list[BaseTool] = [
    get_campaign_recommendations,
    simulate_campaign,
    rank_segments_by_opportunity,
]

_SYSTEM = """\
You are the Campaign Strategy Agent for an ecommerce AI Marketing Platform.

Your role is to design and evaluate marketing campaigns that maximise ROI.

Workflow:
1. Identify the highest-opportunity segments using rank_segments_by_opportunity
2. Retrieve campaign playbooks for those segments using get_campaign_recommendations
3. Simulate the top 2-3 campaign options using simulate_campaign
4. Compare projected ROI, revenue impact and conversion rates
5. Recommend the optimal campaign with clear business justification

Always provide:
- Recommended segment and campaign type
- Budget allocation rationale
- Projected ROI and revenue uplift
- Risk assessment (low/medium/high)
- Implementation timeline suggestion

User query: {user_query}
Data analysis available: {analysis_context}
"""


def campaign_strategy_node(state: AgentState) -> Command:
    start = time.time()
    user_query = state.get("user_query", "")
    analysis_results = state.get("analysis_results", {})
    analysis_context = "; ".join(
        f"{k}: {str(v)[:300]}" for k, v in analysis_results.items()
    ) or "none"

    llm = get_llm()
    agent = create_react_agent(llm, _TOOLS)

    result = agent.invoke({
        "messages": [
            SystemMessage(content=_SYSTEM.format(
                user_query=user_query,
                analysis_context=analysis_context,
            )),
            HumanMessage(content=user_query),
        ]
    })

    output_messages = result.get("messages", [])
    response_text = last_ai_content(output_messages)
    tools_called = extract_tool_names(output_messages)

    trace_step = build_trace_step(
        agent="campaign_strategy",
        action="design campaigns",
        input_summary=user_query,
        output_summary=response_text,
        start_time=start,
        tools_called=tools_called,
    )

    existing_results = state.get("analysis_results", {})
    existing_results["campaign_strategy"] = response_text

    # Parse recommendations from response (simplified)
    recommendations = state.get("recommendations", [])
    recommendations.append({"agent": "campaign_strategy", "content": response_text})

    return Command(
        goto="supervisor",
        update={
            "messages": output_messages,
            "analysis_results": existing_results,
            "recommendations": recommendations,
            "agents_used": list(dict.fromkeys([*state.get("agents_used", []), "campaign_strategy"])),
            "tools_used": list(dict.fromkeys([*state.get("tools_used", []), *tools_called])),
            "execution_trace": [*state.get("execution_trace", []), trace_step],
        },
    )

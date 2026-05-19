"""RAG Knowledge Agent — retrieves marketing best practices from the vector store."""
from __future__ import annotations

import time
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import BaseTool
from langgraph.prebuilt import create_react_agent
from langgraph.types import Command

from app.ai.agents.base import build_trace_step, extract_tool_names, get_llm, last_ai_content
from app.ai.graph.state import AgentState
from app.ai.tools.rag_tools import retrieve_marketing_knowledge

_TOOLS: list[BaseTool] = [retrieve_marketing_knowledge]

_SYSTEM = """\
You are the RAG Knowledge Agent for an AI Marketing Intelligence Platform.

Your role is to retrieve and synthesise relevant marketing knowledge to support business decisions.

Knowledge sources available:
- CRM playbooks and customer lifecycle management guides
- Ecommerce campaign strategy frameworks
- RFM segmentation best practices
- Industry benchmarks (conversion rates, LTV, churn rates)
- Email, loyalty, win-back and cross-sell campaign guides
- Pricing and discount strategy research

When retrieving knowledge:
1. Issue targeted queries for each aspect of the user question
2. Cite the source of each retrieved document
3. Synthesise the information into actionable guidance
4. Flag when retrieved benchmarks may not apply to this specific business context

User query: {user_query}
Existing analysis context: {analysis_context}
"""


def rag_knowledge_node(state: AgentState) -> Command:
    start = time.time()
    user_query = state.get("user_query", "")
    analysis_results = state.get("analysis_results", {})
    analysis_context = "; ".join(
        f"{k}: {str(v)[:200]}" for k, v in analysis_results.items()
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

    # Surface retrieved docs count
    retrieved_docs: list[dict] = []
    for msg in output_messages:
        if hasattr(msg, "content") and isinstance(msg.content, list):
            for item in msg.content:
                if isinstance(item, dict) and "content" in item and not item.get("error"):
                    retrieved_docs.append(item)

    trace_step = build_trace_step(
        agent="rag_knowledge",
        action=f"retrieve docs ({len(retrieved_docs)} found)",
        input_summary=user_query,
        output_summary=response_text,
        start_time=start,
        tools_called=tools_called,
    )

    existing_results = state.get("analysis_results", {})
    existing_results["rag_knowledge"] = response_text

    return Command(
        goto="supervisor",
        update={
            "messages": output_messages,
            "retrieved_docs": [*state.get("retrieved_docs", []), *retrieved_docs],
            "analysis_results": existing_results,
            "agents_used": list(dict.fromkeys([*state.get("agents_used", []), "rag_knowledge"])),
            "tools_used": list(dict.fromkeys([*state.get("tools_used", []), *tools_called])),
            "execution_trace": [*state.get("execution_trace", []), trace_step],
        },
    )

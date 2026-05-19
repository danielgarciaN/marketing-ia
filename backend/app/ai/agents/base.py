"""Base utilities shared by all agent nodes."""
from __future__ import annotations

import time
from typing import Any

from langchain_core.messages import AIMessage, BaseMessage, ToolMessage
from langchain_openai import ChatOpenAI

from app.ai.config import get_ai_settings
from app.ai.graph.state import ExecutionStep


def get_llm(temperature: float | None = None) -> ChatOpenAI:
    """Return a configured ChatOpenAI instance."""
    cfg = get_ai_settings()
    return ChatOpenAI(
        model=cfg.llm_model,
        temperature=temperature if temperature is not None else cfg.llm_temperature,
        max_tokens=cfg.llm_max_tokens,
        api_key=cfg.openai_api_key,
    )


def build_trace_step(
    agent: str,
    action: str,
    input_summary: str,
    output_summary: str,
    start_time: float,
    tools_called: list[str] | None = None,
) -> ExecutionStep:
    return ExecutionStep(
        agent=agent,
        action=action,
        input_summary=input_summary[:200],
        output_summary=output_summary[:500],
        duration_ms=round((time.time() - start_time) * 1000, 1),
        tools_called=tools_called or [],
    )


def extract_tool_names(messages: list[BaseMessage]) -> list[str]:
    """Extract tool names from a sequence of AI + Tool messages."""
    names: list[str] = []
    for msg in messages:
        if isinstance(msg, AIMessage) and msg.tool_calls:
            names.extend(tc["name"] for tc in msg.tool_calls)
    return list(dict.fromkeys(names))  # deduplicate, preserve order


def last_ai_content(messages: list[BaseMessage]) -> str:
    """Return the text content of the last AIMessage in the list."""
    for msg in reversed(messages):
        if isinstance(msg, AIMessage) and isinstance(msg.content, str):
            return msg.content
    return ""

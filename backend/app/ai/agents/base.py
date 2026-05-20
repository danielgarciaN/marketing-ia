"""Utilidades base compartidas por todos los agentes."""
from __future__ import annotations

import time
from typing import Any

from langchain_core.messages import AIMessage, BaseMessage

from app.ai.graph.state import ExecutionStep
from app.ai.llm_factory import get_llm  # noqa: F401 — re-exportado para uso directo en agentes

__all__ = ["get_llm", "build_trace_step", "extract_tool_names", "last_ai_content"]


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
    """Extrae los nombres de herramientas llamadas de una secuencia de mensajes."""
    names: list[str] = []
    for msg in messages:
        if isinstance(msg, AIMessage) and msg.tool_calls:
            names.extend(tc["name"] for tc in msg.tool_calls)
    return list(dict.fromkeys(names))


def last_ai_content(messages: list[BaseMessage]) -> str:
    """Devuelve el contenido textual del último AIMessage de la lista."""
    for msg in reversed(messages):
        if isinstance(msg, AIMessage) and isinstance(msg.content, str):
            return msg.content
    return ""

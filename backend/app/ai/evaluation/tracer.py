"""Observability and tracing for the AI multiagent layer."""
from __future__ import annotations

import logging
import time
from contextlib import contextmanager
from typing import Any, Generator

logger = logging.getLogger("ai.tracer")


class AgentTracer:
    """Lightweight structured tracer for agent execution.

    Emits JSON-compatible log events for each agent turn.
    Integrate with LangSmith, Datadog, or OpenTelemetry via the handlers below.
    """

    def __init__(self, session_id: str, query: str) -> None:
        self.session_id = session_id
        self.query = query
        self.steps: list[dict[str, Any]] = []
        self._start = time.time()

    def record_agent_start(self, agent_name: str, inputs: dict[str, Any]) -> None:
        logger.info(
            "agent_start",
            extra={
                "session_id": self.session_id,
                "agent": agent_name,
                "input_keys": list(inputs.keys()),
            },
        )

    def record_agent_end(self, agent_name: str, outputs: dict[str, Any], duration_ms: float) -> None:
        step = {
            "agent": agent_name,
            "duration_ms": duration_ms,
            "tools_called": outputs.get("tools_used", []),
            "output_length": len(str(outputs.get("final_response", ""))),
        }
        self.steps.append(step)
        logger.info("agent_end", extra={"session_id": self.session_id, **step})

    def record_tool_call(self, tool_name: str, args: dict, result_size: int) -> None:
        logger.debug(
            "tool_call",
            extra={
                "session_id": self.session_id,
                "tool": tool_name,
                "result_size": result_size,
            },
        )

    def record_error(self, agent_name: str, error: str) -> None:
        logger.error(
            "agent_error",
            extra={"session_id": self.session_id, "agent": agent_name, "error": error},
        )

    def summary(self) -> dict[str, Any]:
        elapsed = round((time.time() - self._start) * 1000, 1)
        return {
            "session_id": self.session_id,
            "total_duration_ms": elapsed,
            "total_steps": len(self.steps),
            "steps": self.steps,
        }


@contextmanager
def trace_agent(tracer: AgentTracer, agent_name: str, inputs: dict) -> Generator[None, None, None]:
    """Context manager that records agent start/end automatically."""
    tracer.record_agent_start(agent_name, inputs)
    t0 = time.time()
    try:
        yield
    finally:
        duration = round((time.time() - t0) * 1000, 1)
        tracer.record_agent_end(agent_name, inputs, duration)

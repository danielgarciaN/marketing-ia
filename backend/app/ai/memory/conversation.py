"""Conversation memory — in-process session store (ready for Redis/Postgres upgrade)."""
from __future__ import annotations

import threading
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class ConversationTurn:
    role: str  # "user" | "assistant"
    content: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    metadata: dict[str, Any] = field(default_factory=dict)


class ConversationMemory:
    """Thread-safe in-memory conversation store keyed by session_id.

    Stores the last `max_turns` turns per session.
    Replace the internal dict with Redis for horizontal scaling.
    """

    def __init__(self, max_turns: int = 20) -> None:
        self._max_turns = max_turns
        self._sessions: dict[str, deque[ConversationTurn]] = {}
        self._lock = threading.Lock()

    def add_turn(self, session_id: str, role: str, content: str, metadata: dict | None = None) -> None:
        with self._lock:
            if session_id not in self._sessions:
                self._sessions[session_id] = deque(maxlen=self._max_turns)
            self._sessions[session_id].append(
                ConversationTurn(role=role, content=content, metadata=metadata or {})
            )

    def get_history(self, session_id: str) -> list[ConversationTurn]:
        with self._lock:
            return list(self._sessions.get(session_id, []))

    def get_context_window(self, session_id: str, last_n: int = 6) -> str:
        """Return the last N turns formatted as a context string for the LLM."""
        history = self.get_history(session_id)[-last_n:]
        return "\n".join(f"{t.role.upper()}: {t.content}" for t in history)

    def clear_session(self, session_id: str) -> None:
        with self._lock:
            self._sessions.pop(session_id, None)

    def session_exists(self, session_id: str) -> bool:
        return session_id in self._sessions

    @property
    def active_sessions(self) -> int:
        return len(self._sessions)


# Singleton for the application lifecycle
memory_store = ConversationMemory(max_turns=30)

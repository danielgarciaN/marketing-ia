"""Configuración centralizada para la capa multiagente de IA."""
from functools import lru_cache
from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict


class AISettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # ── Proveedor LLM ─────────────────────────────────────────────────────────
    llm_provider: Literal["openai", "ollama", "mock"] = "ollama"
    llm_temperature: float = 0.0
    llm_max_tokens: int = 4096

    # ── OpenAI ────────────────────────────────────────────────────────────────
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    openai_embedding_model: str = "text-embedding-3-small"

    # ── Ollama ────────────────────────────────────────────────────────────────
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.1:8b"
    ollama_embedding_model: str = "nomic-embed-text"

    # ── Embeddings ────────────────────────────────────────────────────────────
    embedding_provider: Literal["openai", "ollama", "mock"] = "ollama"

    # ── RAG / Qdrant ─────────────────────────────────────────────────────────
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: str = ""
    qdrant_collection: str = "marketing_knowledge"
    rag_top_k: int = 5
    rag_score_threshold: float = 0.5   # umbral más bajo para embeddings locales
    chunk_size: int = 512
    chunk_overlap: int = 64

    # ── Ejecución del grafo ───────────────────────────────────────────────────
    max_iterations: int = 12
    recursion_limit: int = 50

    # ── Observabilidad ────────────────────────────────────────────────────────
    langsmith_api_key: str = ""
    langsmith_project: str = "marketing-ai-agents"
    langsmith_tracing: bool = False

    # ── Compatibilidad con variables antiguas ─────────────────────────────────
    # Estas variables legacy son ignoradas — se mantienen por si hay un .env antiguo
    llm_model: str = ""
    embedding_model: str = ""

    @property
    def embedding_dim(self) -> int:
        """Dimensión del vector de embeddings según el proveedor."""
        if self.embedding_provider == "openai":
            return 1536  # text-embedding-3-small
        return 768  # nomic-embed-text (Ollama) y mock


@lru_cache
def get_ai_settings() -> AISettings:
    return AISettings()

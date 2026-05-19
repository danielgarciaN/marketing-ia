"""Centralised configuration for the AI multiagent layer."""
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class AISettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # LLM
    openai_api_key: str = ""
    llm_model: str = "gpt-4o-mini"
    llm_temperature: float = 0.0
    llm_max_tokens: int = 4096

    # RAG / Vector Store
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: str = ""
    qdrant_collection: str = "marketing_knowledge"
    embedding_model: str = "text-embedding-3-small"
    rag_top_k: int = 5
    rag_score_threshold: float = 0.65
    chunk_size: int = 512
    chunk_overlap: int = 64

    # Graph execution
    max_iterations: int = 12
    recursion_limit: int = 50

    # Observability
    langsmith_api_key: str = ""
    langsmith_project: str = "marketing-ai-agents"
    langsmith_tracing: bool = False


@lru_cache
def get_ai_settings() -> AISettings:
    return AISettings()

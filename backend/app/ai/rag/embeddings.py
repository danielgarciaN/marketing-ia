"""Embedding model factory for the RAG pipeline."""
from __future__ import annotations

from functools import lru_cache

from langchain_openai import OpenAIEmbeddings

from app.ai.config import get_ai_settings


@lru_cache(maxsize=1)
def get_embeddings() -> OpenAIEmbeddings:
    """Return a singleton OpenAI Embeddings instance."""
    cfg = get_ai_settings()
    return OpenAIEmbeddings(
        model=cfg.embedding_model,
        api_key=cfg.openai_api_key,
    )

"""Fábrica de embeddings para el pipeline RAG.

Delega en llm_factory.get_embeddings() que respeta EMBEDDING_PROVIDER del .env.
Este módulo se mantiene por compatibilidad — importa directamente de llm_factory
si prefieres.
"""
from __future__ import annotations

from langchain_core.embeddings import Embeddings

from app.ai.llm_factory import get_embeddings

__all__ = ["get_embeddings"]

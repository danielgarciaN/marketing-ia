"""Qdrant vector store interface."""
from __future__ import annotations

from functools import lru_cache

from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from app.ai.config import get_ai_settings
from app.ai.rag.embeddings import get_embeddings

EMBEDDING_DIM = 1536  # text-embedding-3-small


def get_qdrant_client() -> QdrantClient:
    cfg = get_ai_settings()
    return QdrantClient(url=cfg.qdrant_url, api_key=cfg.qdrant_api_key or None)


def ensure_collection_exists(client: QdrantClient, collection_name: str) -> None:
    """Create the Qdrant collection if it does not already exist."""
    existing = {c.name for c in client.get_collections().collections}
    if collection_name not in existing:
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=EMBEDDING_DIM, distance=Distance.COSINE),
        )


@lru_cache(maxsize=1)
def get_vector_store() -> QdrantVectorStore:
    """Return a singleton QdrantVectorStore connected to the marketing knowledge collection."""
    cfg = get_ai_settings()
    client = get_qdrant_client()
    ensure_collection_exists(client, cfg.qdrant_collection)
    return QdrantVectorStore(
        client=client,
        collection_name=cfg.qdrant_collection,
        embedding=get_embeddings(),
    )

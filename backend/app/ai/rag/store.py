"""Interfaz con el vector store Qdrant."""
from __future__ import annotations

from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from app.ai.config import get_ai_settings
from app.ai.llm_factory import get_embeddings


def _embedding_dim() -> int:
    """Dimensión del vector según el proveedor configurado.

    - OpenAI text-embedding-3-small: 1536
    - Ollama nomic-embed-text:       768
    - Mock:                          768
    """
    return get_ai_settings().embedding_dim


def get_qdrant_client() -> QdrantClient:
    cfg = get_ai_settings()
    return QdrantClient(url=cfg.qdrant_url, api_key=cfg.qdrant_api_key or None)


def ensure_collection_exists(client: QdrantClient, collection_name: str) -> None:
    """Crea la colección Qdrant si no existe, con la dimensión correcta."""
    existing = {c.name for c in client.get_collections().collections}
    if collection_name not in existing:
        dim = _embedding_dim()
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=dim, distance=Distance.COSINE),
        )


def get_vector_store() -> QdrantVectorStore:
    """Devuelve un QdrantVectorStore con el modelo de embeddings configurado.

    Nota: no se usa @lru_cache aquí porque get_embeddings() ya gestiona
    la creación del modelo. Cambiar EMBEDDING_PROVIDER requiere reiniciar.
    """
    cfg = get_ai_settings()
    client = get_qdrant_client()
    ensure_collection_exists(client, cfg.qdrant_collection)
    return QdrantVectorStore(
        client=client,
        collection_name=cfg.qdrant_collection,
        embedding=get_embeddings(),
    )

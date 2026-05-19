"""Retriever factory — creates LangChain-compatible retrievers from the vector store."""
from __future__ import annotations

from langchain_core.vectorstores import VectorStoreRetriever

from app.ai.config import get_ai_settings
from app.ai.rag.store import get_vector_store


def get_retriever(top_k: int | None = None) -> VectorStoreRetriever:
    """Return a similarity-score-threshold retriever backed by Qdrant.

    Args:
        top_k: Number of documents to retrieve. Defaults to config value.
    """
    cfg = get_ai_settings()
    store = get_vector_store()
    k = top_k or cfg.rag_top_k

    return store.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={
            "k": k,
            "score_threshold": cfg.rag_score_threshold,
        },
    )


def get_mmr_retriever(top_k: int | None = None, fetch_k: int = 20) -> VectorStoreRetriever:
    """Return a Maximal Marginal Relevance retriever for diversity-aware retrieval.

    Useful when multiple documents on the same topic might otherwise dominate results.
    """
    cfg = get_ai_settings()
    store = get_vector_store()
    k = top_k or cfg.rag_top_k

    return store.as_retriever(
        search_type="mmr",
        search_kwargs={"k": k, "fetch_k": fetch_k, "lambda_mult": 0.6},
    )

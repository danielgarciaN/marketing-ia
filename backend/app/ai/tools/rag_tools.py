"""RAG retrieval tool — surfaces relevant marketing knowledge for any agent."""
from __future__ import annotations

from typing import Any
from langchain_core.tools import tool


@tool
def retrieve_marketing_knowledge(query: str, top_k: int = 4) -> list[dict[str, Any]]:
    """Retrieve relevant marketing and ecommerce knowledge from the vector database.

    Searches through CRM playbooks, campaign guides, benchmarks, and best practices.
    Returns documents with content and citation metadata.

    Args:
        query: Semantic search query (topic, question, or keyword)
        top_k: Number of documents to retrieve (1–10)
    """
    try:
        from app.ai.rag.retriever import get_retriever
        retriever = get_retriever(top_k=min(top_k, 10))
        docs = retriever.invoke(query)
        return [
            {
                "content": doc.page_content,
                "source": doc.metadata.get("source", "unknown"),
                "page": doc.metadata.get("page"),
                "score": doc.metadata.get("score"),
                "doc_type": doc.metadata.get("doc_type", "general"),
            }
            for doc in docs
        ]
    except Exception as exc:
        # Graceful degradation: RAG is unavailable (Qdrant not running, no docs ingested)
        return [
            {
                "content": f"RAG service unavailable: {exc}",
                "source": "system",
                "error": True,
            }
        ]

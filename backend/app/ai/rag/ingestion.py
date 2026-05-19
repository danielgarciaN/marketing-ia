"""Document ingestion pipeline: load → chunk → embed → store in Qdrant."""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from langchain_community.document_loaders import PyPDFLoader, TextLoader, UnstructuredMarkdownLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.ai.config import get_ai_settings
from app.ai.rag.store import get_vector_store

logger = logging.getLogger(__name__)

SUPPORTED_EXTENSIONS = {".pdf", ".md", ".txt"}

# Default knowledge base directory (relative to backend root)
KNOWLEDGE_DIR = Path(__file__).parent / "docs"


def _load_document(file_path: Path) -> list[Document]:
    """Load a single document using the appropriate loader."""
    suffix = file_path.suffix.lower()
    if suffix == ".pdf":
        loader = PyPDFLoader(str(file_path))
    elif suffix == ".md":
        loader = UnstructuredMarkdownLoader(str(file_path))
    else:
        loader = TextLoader(str(file_path), encoding="utf-8")
    docs = loader.load()
    for doc in docs:
        doc.metadata["source"] = file_path.name
        doc.metadata["doc_type"] = suffix.lstrip(".")
    return docs


def _chunk_documents(documents: list[Document]) -> list[Document]:
    cfg = get_ai_settings()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=cfg.chunk_size,
        chunk_overlap=cfg.chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    return splitter.split_documents(documents)


def ingest_directory(directory: Path | None = None) -> dict[str, Any]:
    """Ingest all supported documents from a directory into Qdrant.

    Args:
        directory: Path to scan. Defaults to the bundled docs/ folder.

    Returns:
        Summary dict with files processed, chunks ingested, errors.
    """
    target_dir = directory or KNOWLEDGE_DIR
    target_dir.mkdir(parents=True, exist_ok=True)

    results: dict[str, Any] = {"files": [], "total_chunks": 0, "errors": []}
    all_chunks: list[Document] = []

    for file_path in sorted(target_dir.rglob("*")):
        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue
        try:
            docs = _load_document(file_path)
            chunks = _chunk_documents(docs)
            all_chunks.extend(chunks)
            results["files"].append({"file": file_path.name, "chunks": len(chunks)})
            logger.info("Loaded %s → %d chunks", file_path.name, len(chunks))
        except Exception as exc:
            results["errors"].append({"file": str(file_path), "error": str(exc)})
            logger.exception("Failed to load %s", file_path)

    if all_chunks:
        store = get_vector_store()
        store.add_documents(all_chunks)
        results["total_chunks"] = len(all_chunks)
        logger.info("Ingested %d total chunks into Qdrant", len(all_chunks))

    return results


def ingest_file(file_path: Path) -> dict[str, Any]:
    """Ingest a single file into the vector store."""
    docs = _load_document(file_path)
    chunks = _chunk_documents(docs)
    store = get_vector_store()
    store.add_documents(chunks)
    return {"file": file_path.name, "chunks_ingested": len(chunks)}

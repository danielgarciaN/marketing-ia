"""Fábrica centralizada de LLMs y Embeddings.

Controla qué proveedor se usa mediante la variable de entorno LLM_PROVIDER:
  - openai  → ChatOpenAI + OpenAIEmbeddings  (requiere OPENAI_API_KEY)
  - ollama  → ChatOllama + OllamaEmbeddings  (requiere Ollama en localhost)
  - mock    → Modelos simulados sin llamadas externas (para desarrollo)
"""
from __future__ import annotations

import time
from typing import Any

from langchain_core.embeddings import Embeddings
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage
from langchain_core.outputs import ChatGeneration, ChatResult

from app.ai.config import get_ai_settings


# ══════════════════════════════════════════════════════════════════════════════
# LLM FACTORY
# ══════════════════════════════════════════════════════════════════════════════

def get_llm(temperature: float | None = None) -> BaseChatModel:
    """Devuelve un LLM configurado según LLM_PROVIDER en .env.

    Args:
        temperature: Sobrescribe la temperatura de configuración si se especifica.

    Returns:
        ChatOpenAI | ChatOllama | MockChatModel
    """
    cfg = get_ai_settings()
    temp = temperature if temperature is not None else cfg.llm_temperature

    if cfg.llm_provider == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model=cfg.openai_model,
            temperature=temp,
            max_tokens=cfg.llm_max_tokens,
            api_key=cfg.openai_api_key,
        )

    if cfg.llm_provider == "ollama":
        from langchain_ollama import ChatOllama
        return ChatOllama(
            model=cfg.ollama_model,
            temperature=temp,
            base_url=cfg.ollama_base_url,
            num_predict=cfg.llm_max_tokens,
        )

    if cfg.llm_provider == "mock":
        return MockChatModel()

    raise ValueError(
        f"LLM_PROVIDER inválido: '{cfg.llm_provider}'. "
        "Opciones válidas: openai | ollama | mock"
    )


# ══════════════════════════════════════════════════════════════════════════════
# EMBEDDINGS FACTORY
# ══════════════════════════════════════════════════════════════════════════════

def get_embeddings() -> Embeddings:
    """Devuelve un modelo de embeddings según EMBEDDING_PROVIDER en .env.

    Returns:
        OpenAIEmbeddings | OllamaEmbeddings | MockEmbeddings
    """
    cfg = get_ai_settings()

    if cfg.embedding_provider == "openai":
        from langchain_openai import OpenAIEmbeddings
        return OpenAIEmbeddings(
            model=cfg.openai_embedding_model,
            api_key=cfg.openai_api_key,
        )

    if cfg.embedding_provider == "ollama":
        from langchain_ollama import OllamaEmbeddings
        return OllamaEmbeddings(
            model=cfg.ollama_embedding_model,
            base_url=cfg.ollama_base_url,
        )

    if cfg.embedding_provider == "mock":
        return MockEmbeddings()

    raise ValueError(
        f"EMBEDDING_PROVIDER inválido: '{cfg.embedding_provider}'. "
        "Opciones válidas: openai | ollama | mock"
    )


# ══════════════════════════════════════════════════════════════════════════════
# MOCK LLM
# ══════════════════════════════════════════════════════════════════════════════

_MOCK_RESPONSE = (
    "[MODO MOCK] Análisis de marketing completado en modo demostración.\n\n"
    "**Segmento prioritario:** At-Risk (clientes con alta compra histórica y baja recencia)\n\n"
    "**Campaña recomendada:** Win-Back con 15% de descuento por tiempo limitado.\n\n"
    "**ROI estimado:** 150–200% sobre inversión de €5,000.\n\n"
    "**Acciones inmediatas:**\n"
    "1. Lanzar campaña de email personalizado a los 847 clientes At-Risk\n"
    "2. Ofrecer descuento exclusivo de 15% válido 7 días\n"
    "3. Seguimiento por SMS a los no-abiertos a los 3 días\n\n"
    "_Este es un modo de demostración. Configura LLM_PROVIDER=ollama o LLM_PROVIDER=openai para respuestas reales._"
)


class MockChatModel(BaseChatModel):
    """LLM simulado para desarrollo y testing sin coste ni dependencias externas."""

    mock_response: str = _MOCK_RESPONSE

    def _generate(
        self,
        messages: list,
        stop: list[str] | None = None,
        run_manager: Any = None,
        **kwargs: Any,
    ) -> ChatResult:
        ai_msg = AIMessage(content=self.mock_response)
        return ChatResult(generations=[ChatGeneration(message=ai_msg)])

    @property
    def _llm_type(self) -> str:
        return "mock"

    def bind_tools(self, tools: list, **kwargs: Any) -> "MockChatModel":
        return self

    def with_structured_output(
        self,
        schema: Any,
        *,
        include_raw: bool = False,
        **kwargs: Any,
    ) -> Any:
        """Devuelve un runnable que produce una instancia por defecto del schema."""
        from langchain_core.runnables import RunnableLambda

        def produce_mock(_input: Any) -> Any:
            if not hasattr(schema, "model_fields"):
                try:
                    return schema()
                except Exception:
                    return {}

            defaults: dict[str, Any] = {}
            for field_name, field_info in schema.model_fields.items():
                if field_name == "next_agent":
                    defaults[field_name] = "data_analyst"
                elif field_name == "intent":
                    defaults[field_name] = "analytics"
                elif field_name in ("reasoning", "description", "explanation", "summary"):
                    defaults[field_name] = "[MOCK] Enrutando al agente de análisis de datos."
                elif field_info.default is not None:
                    from pydantic_core import PydanticUndefinedType
                    if not isinstance(field_info.default, PydanticUndefinedType):
                        defaults[field_name] = field_info.default

            try:
                return schema(**defaults)
            except Exception:
                return schema.model_construct(**defaults)

        return RunnableLambda(produce_mock)


# ══════════════════════════════════════════════════════════════════════════════
# MOCK EMBEDDINGS
# ══════════════════════════════════════════════════════════════════════════════

class MockEmbeddings(Embeddings):
    """Embeddings simulados (vectores constantes) para testing sin modelos externos."""

    dim: int = 768

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [[0.01] * self.dim for _ in texts]

    def embed_query(self, text: str) -> list[float]:
        return [0.01] * self.dim

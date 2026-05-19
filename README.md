# AI Marketing Intelligence Platform

**Enterprise-grade customer intelligence platform powered by a LangGraph multiagent AI system.**

Transforms raw ecommerce transaction data into actionable marketing strategy through autonomous AI agents, RAG-backed knowledge retrieval, and data-driven campaign simulation.

---

## What This Is

A production-ready SaaS platform that combines classical ML analytics with a modern multiagent AI layer:

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Analytics** | Pandas · Scikit-learn | RFM scoring, KMeans clustering, segment KPIs |
| **API** | FastAPI · Pydantic v2 | REST endpoints for dashboard and analytics |
| **AI Agents** | LangGraph · LangChain | Autonomous reasoning and orchestration |
| **RAG** | Qdrant · OpenAI Embeddings | Marketing knowledge retrieval with citations |
| **Frontend** | Next.js · Recharts | Interactive dashboards and campaign simulator |

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                    FASTAPI APPLICATION (v2.0)                        │
│                                                                       │
│  /dashboard  /customers  /segments  /campaigns  /insights  /model    │
│                         ↓ NEW                                        │
│              ┌──────────────────────────┐                            │
│              │    /ai  — AI Layer        │                            │
│              │  POST /ai/query           │                            │
│              │  POST /ai/report          │                            │
│              │  POST /ai/recommendations │                            │
│              │  GET  /ai/conversations   │                            │
│              │  GET  /ai/traces          │                            │
│              │  POST /ai/rag/ingest      │                            │
│              └──────────┬───────────────┘                            │
└─────────────────────────┼───────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   LANGGRAPH MULTIAGENT ENGINE                         │
│                                                                       │
│   START ──► SUPERVISOR ─────────────────────────────────────────┐   │
│                │                                                  │   │
│                │ Command(goto=next_agent)                         │   │
│                ▼                                                  │   │
│   ┌────────────────────────────────────────────────────────┐     │   │
│   │                    WORKER AGENTS                        │     │   │
│   │                                                         │     │   │
│   │  ┌──────────────┐  ┌─────────────┐  ┌───────────────┐  │     │   │
│   │  │ DATA ANALYST │  │ SQL/PANDAS  │  │ RAG KNOWLEDGE │  │     │   │
│   │  │ KPIs·trends  │  │queries·filt │  │best practices │  │     │   │
│   │  │ segments·RFM │  │ers·metrics  │  │benchmarks·CRM │  │     │   │
│   │  └──────────────┘  └─────────────┘  └───────────────┘  │     │   │
│   │                                                         │     │   │
│   │  ┌──────────────┐  ┌─────────────┐                     │     │   │
│   │  │  CAMPAIGN    │  │ FORECASTING │                     │     │   │
│   │  │  STRATEGY    │  │revenue·LTV  │                     │     │   │
│   │  │  ROI·budget  │  │churn·trends │                     │     │   │
│   │  └──────────────┘  └─────────────┘                     │     │   │
│   └────────────────────────┬───────────────────────────────┘     │   │
│                             │ Command(goto="supervisor")           │   │
│                             └──────────────────────────────────────┘   │
│                                      │ (when done)                    │
│                                      ▼                                │
│                          ┌───────────────────┐                       │
│                          │ INSIGHT NARRATOR   │                       │
│                          │ executive summary  │                       │
│                          │ business language  │                       │
│                          └─────────┬─────────┘                       │
│                                    │                                  │
│                                   END                                │
└─────────────────────────────────────────────────────────────────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │   QDRANT VECTOR DB    │
              │ marketing_knowledge   │
              │ CRM playbooks · PDFs  │
              │ campaign guides · MD  │
              └───────────────────────┘
```

---

## How LangGraph Works Here

LangGraph is a graph execution framework for building stateful, multi-step AI workflows.

**Key concepts used in this project:**

- **StateGraph** — a directed graph where each node is an agent function
- **AgentState** — a shared TypedDict that all agents read from and write to
- **Command(goto=...)** — agents return routing instructions, not just data
- **Conditional edges** — the supervisor decides the next node at every step
- **add_messages** reducer — messages accumulate safely across parallel runs

**Why LangGraph instead of a simple chain?**

| Problem | LangGraph solution |
|---------|-------------------|
| Complex routing logic | Conditional edges + supervisor pattern |
| State shared across agents | Single `AgentState` TypedDict |
| Tool use per agent | `create_react_agent` with typed tools |
| Safety / loops | `recursion_limit` + `iteration_count` guard |
| Observability | `execution_trace` built into state |

---

## Agents

### Supervisor
Routes every query to the right sequence of agents. Uses structured LLM output (`RoutingDecision`) to classify intent and decide the next node. Enforces the max-iteration safety limit.

**Intents classified:** `analytics` · `segmentation` · `campaign` · `forecast` · `knowledge` · `report` · `general`

### Data Analyst
Retrieves KPIs, segment summaries, revenue trends, and RFM distributions via tool calls against the existing DataService.

**Tools:** `get_dashboard_summary` · `get_segment_overview` · `compute_segment_stats` · `get_revenue_trend`

### SQL/Pandas Agent
Executes dynamic Pandas query expressions against the customer dataset. Enables ad-hoc filtering without hardcoded queries.

**Tools:** `run_pandas_query` · `get_rfm_distribution` · `get_customer_by_id`

### RAG Knowledge Agent
Retrieves relevant marketing knowledge from Qdrant. Surfaces CRM playbooks, campaign guides, and benchmarks with source citations.

**Tools:** `retrieve_marketing_knowledge`

### Campaign Strategy Agent
Ranks segments by opportunity, retrieves playbooks, simulates ROI for multiple scenarios, and produces prioritised recommendations.

**Tools:** `rank_segments_by_opportunity` · `get_campaign_recommendations` · `simulate_campaign`

### Forecasting Agent
Projects future revenue (linear trend), estimates churn risk (recency heuristics), and calculates Customer Lifetime Value per segment.

**Tools:** `forecast_revenue` · `predict_churn_risk` · `estimate_ltv`

### Insight Narrator
Synthesises all agent outputs into a single executive narrative. Always the final step before `END`.

---

## Shared State

```python
class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    session_id: str
    user_query: str
    intent: Intent                        # classified by supervisor
    active_agent: AgentName
    next_agent: AgentName
    agents_used: list[str]                # execution history
    tools_used: list[str]                 # tool call audit trail
    iteration_count: int                  # safety guard (max 12)
    execution_trace: list[ExecutionStep]  # full observability
    retrieved_docs: list[dict]            # RAG results with citations
    analysis_results: dict                # keyed by agent name
    recommendations: list[dict]
    forecast_data: dict
    final_response: str
    confidence_score: float               # 0.0 – 1.0
    error: str | None
```

---

## RAG Pipeline

```
Documents (PDF · MD · TXT)
      │
      ▼  PyPDFLoader / UnstructuredMarkdownLoader / TextLoader
 Raw Documents
      │
      ▼  RecursiveCharacterTextSplitter (512 tokens, 64 overlap)
 Text Chunks
      │
      ▼  OpenAI text-embedding-3-small (1536 dimensions)
 Embeddings
      │
      ▼  upsert → Qdrant collection: marketing_knowledge
 Vector Store
      │
      ▼  similarity_score_threshold retrieval (top-5, score ≥ 0.65)
 Relevant Chunks → cited in agent response
```

Documents to add: CRM playbooks · campaign strategy guides · ecommerce benchmarks · RFM best practices

---

## Example Flow

**Query:** *"¿Qué segmento de clientes deberíamos priorizar este mes y qué campaña lanzar?"*

```
1. SUPERVISOR       classify intent → "campaign"
                    route → data_analyst

2. DATA ANALYST     get_segment_overview()
                    compute_segment_stats("At-Risk")
                    → At-Risk: 847 customers, €142K revenue at stake

3. SUPERVISOR       route → rag_knowledge

4. RAG KNOWLEDGE    retrieve_marketing_knowledge("win-back campaign best practices")
                    → 4 docs: re-engagement timing, discount thresholds, benchmarks

5. SUPERVISOR       route → campaign_strategy

6. CAMPAIGN STR.    rank_segments_by_opportunity(metric="risk")
                    simulate_campaign("At-Risk", "Win-Back", budget=5000, discount=15%)
                    → ROI: 187%, conversions: 203, revenue uplift: €31,400

7. SUPERVISOR       route → insight_narrator

8. INSIGHT NARR.    synthesise → "Recomendamos priorizar el segmento At-Risk
                    (847 clientes, €142K en riesgo). Una campaña Win-Back con 15%
                    de descuento proyecta un ROI del 187% sobre €5,000 invertidos..."

9. END              confidence_score: 0.94
                    agents_used: 5 · tools_used: 7 · docs_retrieved: 4
```

---

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/ai/query` | Natural language question → multiagent response |
| `POST` | `/ai/report` | Generate structured business report |
| `POST` | `/ai/recommendations` | AI-powered campaign recommendations |
| `GET` | `/ai/conversations/{id}` | Retrieve session history |
| `GET` | `/ai/traces/{id}` | Agent execution audit log |
| `DELETE` | `/ai/conversations/{id}` | Clear session |
| `POST` | `/ai/rag/ingest` | Ingest documents into knowledge base |
| `GET` | `/ai/health` | AI layer health check |

**POST /ai/query — example:**

```json
// Request
{ "query": "¿Qué segmento priorizar este mes?", "session_id": null }

// Response
{
  "session_id": "3fa1b2c4-...",
  "intent": "campaign",
  "response": "## Recomendación Ejecutiva\n\n**At-Risk** debe ser la prioridad...",
  "agents_used": ["supervisor", "data_analyst", "campaign_strategy", "insight_narrator"],
  "tools_used": ["get_segment_overview", "simulate_campaign", "retrieve_marketing_knowledge"],
  "confidence_score": 0.94,
  "retrieved_docs_count": 4
}
```

---

## Project Structure

```
marketing-ia/
├── backend/
│   ├── app/
│   │   ├── api/                      # Existing analytics routes
│   │   ├── ml/                       # RFM, clustering, preprocessing
│   │   ├── services/                 # DataService, SimulatorService
│   │   ├── models/                   # Pydantic schemas (existing)
│   │   └── ai/                       # ← NEW: Multiagent AI layer
│   │       ├── config.py             # pydantic-settings, .env
│   │       ├── agents/
│   │       │   ├── base.py           # LLM factory + trace helpers
│   │       │   ├── supervisor.py     # Intent routing (structured output)
│   │       │   ├── data_analyst.py   # KPI + segment analysis
│   │       │   ├── sql_pandas.py     # Dynamic Pandas queries
│   │       │   ├── rag_knowledge.py  # RAG-backed retrieval
│   │       │   ├── campaign_strategy.py  # Campaign design + ROI sim
│   │       │   ├── forecasting.py    # Revenue + churn + LTV
│   │       │   └── insight_narrator.py   # Executive narrative
│   │       ├── graph/
│   │       │   ├── state.py          # AgentState TypedDict
│   │       │   ├── builder.py        # StateGraph assembly
│   │       │   ├── edges.py          # Conditional routing helpers
│   │       │   └── executor.py       # Async graph runner
│   │       ├── rag/
│   │       │   ├── embeddings.py     # OpenAI embedding factory
│   │       │   ├── store.py          # Qdrant vector store
│   │       │   ├── ingestion.py      # Load → chunk → embed → store
│   │       │   ├── retriever.py      # Similarity + MMR retrievers
│   │       │   └── docs/             # Place knowledge docs here
│   │       ├── tools/
│   │       │   ├── data_tools.py     # Dashboard + customer access
│   │       │   ├── analytics_tools.py    # Pandas computation
│   │       │   ├── campaign_tools.py     # Recommendations + ROI sim
│   │       │   ├── forecasting_tools.py  # Revenue + churn + LTV
│   │       │   ├── report_tools.py       # Report formatting
│   │       │   └── rag_tools.py          # Knowledge retrieval
│   │       ├── memory/
│   │       │   └── conversation.py   # Thread-safe session store
│   │       ├── schemas/
│   │       │   ├── requests.py       # AIQueryRequest, AIReportRequest
│   │       │   └── responses.py      # AIQueryResponse, AITraceResponse
│   │       ├── services/
│   │       │   └── ai_service.py     # Orchestration + memory bridge
│   │       ├── evaluation/
│   │       │   └── tracer.py         # Structured agent tracing
│   │       └── api/
│   │           └── routes_ai.py      # FastAPI AI route handlers
│   ├── requirements.txt
│   └── .env.example
├── frontend/                         # Next.js dashboard
├── notebooks/                        # Jupyter analysis
└── docs/                             # Architecture documentation
```

---

## Installation

### Requirements
- Python 3.11+
- Node.js 18+
- Docker
- OpenAI API key

### 1. Backend dependencies

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

### 2. Environment variables

```bash
cp .env.example .env
# Add your OPENAI_API_KEY in .env
```

### 3. Start Qdrant (vector database)

```bash
docker run -p 6333:6333 qdrant/qdrant
```

### 4. Ingest knowledge base (optional but recommended)

Add `.pdf`, `.md`, or `.txt` files to `backend/app/ai/rag/docs/`, then:

```bash
curl -X POST http://localhost:8000/ai/rag/ingest
```

### 5. Run the API

```bash
uvicorn app.main:app --reload --port 8000
```

API docs available at [http://localhost:8000/docs](http://localhost:8000/docs)

### 6. Frontend

```bash
cd frontend
npm install && npm run dev
```

---

## Why Enterprise-Grade

| Property | Implementation |
|----------|---------------|
| **Modularity** | One file per agent, one responsibility per module |
| **Extensibility** | New agent = one file + one line in `builder.py` |
| **Observability** | Full `execution_trace` per query: agent, tool, duration |
| **Safety** | Iteration cap (12), error isolation, graceful degradation |
| **Memory** | Thread-safe session store, drop-in Redis/Postgres upgrade |
| **RAG quality** | Score-threshold filtering, MMR for diversity, citations |
| **Type safety** | End-to-end TypedDict state, Pydantic v2, strict annotations |
| **Async** | Fully async graph via `ainvoke` + `astream_events` ready |
| **Config** | `pydantic-settings` + `.env`, zero hardcoded secrets |
| **Routing** | `Command(goto=...)` pattern — supervisor owns all transitions |

---

## Roadmap

**Phase 2 — Memory & Persistence**
- Redis-backed session memory for horizontal scaling
- PostgreSQL conversation history
- LangGraph `checkpointer` for multi-turn stateful workflows

**Phase 3 — Advanced AI**
- Human-in-the-loop (`interrupt`) for high-stakes decisions
- Streaming via SSE (`astream_events`)
- LangSmith tracing integration
- Agent evaluation suite with ground-truth assertions

**Phase 4 — Production**
- Docker Compose (API + Qdrant + Redis)
- Kubernetes deployment manifests
- Auth middleware on `/ai` routes
- Prometheus + Grafana observability stack

---

## Tech Stack

**Backend:** Python 3.11 · FastAPI · Pydantic v2 · Pandas · Scikit-learn · Joblib

**AI:** LangGraph 0.2 · LangChain 0.3 · OpenAI GPT-4o-mini · text-embedding-3-small

**RAG:** Qdrant · RecursiveCharacterTextSplitter · PyPDF · Unstructured

**Frontend:** Next.js 14 · React 18 · TypeScript · Recharts · Lucide

**Infrastructure:** Docker · Uvicorn · (Redis · Postgres — roadmap)

---

*Portfolio demonstration of enterprise AI engineering: multiagent orchestration with LangGraph, production RAG pipeline, clean architecture, and real business value.*

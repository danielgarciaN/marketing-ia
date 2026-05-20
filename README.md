# AI Marketing Intelligence Platform

**Plataforma enterprise de inteligencia de marketing impulsada por un sistema multiagente LangGraph con soporte para modelos locales gratuitos mediante Ollama.**

Transforma datos transaccionales de ecommerce en estrategia de marketing accionable a través de agentes autónomos de IA, recuperación de conocimiento RAG y simulación de campañas basada en datos.

---

## ¿Qué es este proyecto?

Un sistema de analítica de marketing que combina:

1. **Analítica clásica de ML**: scoring RFM, clustering KMeans, segmentación de clientes
2. **Capa de IA multiagente**: agentes especializados que razonan, colaboran y producen respuestas de negocio
3. **RAG (Retrieval-Augmented Generation)**: recuperación de conocimiento desde una base documental en Qdrant
4. **API REST completa**: FastAPI con todos los endpoints de analítica y la capa de IA
5. **Dashboard interactivo**: Next.js con visualizaciones, simulador de campañas y gestor de datos

**Lo más importante**: funciona completamente gratis usando Ollama con modelos locales. No necesitas API key de OpenAI para probarlo.

---

## ¿Qué problema resuelve?

Los equipos de marketing de ecommerce necesitan:
- Saber **qué segmento priorizar** en cada momento
- Entender **qué campaña lanzar** y con qué presupuesto
- Predecir **qué clientes van a abandonar**
- Acceder a **conocimiento estratégico de CRM** sin buscar en documentos

Esta plataforma convierte esas preguntas en lenguaje natural en análisis automáticos, recomendaciones de campaña con ROI estimado y narrativas ejecutivas listas para presentar.

---

## ¿Cómo funciona?

```
Tú preguntas:
"¿Qué segmento priorizar este mes y qué campaña lanzar?"
          │
          ▼
┌─────────────────────┐
│   POST /ai/query    │  ← API FastAPI
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────┐
│                MOTOR LANGGRAPH MULTIAGENTE                   │
│                                                              │
│  SUPERVISOR ──► DATA ANALYST ──► RAG KNOWLEDGE              │
│      │                                                       │
│      └──────► CAMPAIGN STRATEGY ──► INSIGHT NARRATOR ──► FIN│
└─────────────────────────────────────────────────────────────┘
           │
           ▼
Respuesta ejecutiva con:
- Segmento At-Risk identificado (847 clientes, €142K en riesgo)
- Campaña Win-Back recomendada con 15% descuento
- ROI proyectado: 187% sobre inversión de €5.000
- Fuentes de conocimiento citadas (playbooks CRM)
```

---

## ¿Cómo funciona LangGraph aquí?

LangGraph es el motor de orquestación que conecta todos los agentes.

**Conceptos clave**:

| Concepto | Qué hace en este proyecto |
|---|---|
| `StateGraph` | Define el grafo de agentes como máquina de estados |
| `AgentState` | TypedDict compartido que todos los agentes leen y escriben |
| `Command(goto=...)` | Cada agente decide dinámicamente quién actúa después |
| `create_react_agent` | Permite a cada agente usar herramientas (tools) de forma autónoma |

**Flujo real**:
1. `START → supervisor` → clasifica la intención de la pregunta
2. `supervisor → data_analyst` → analiza KPIs y segmentos
3. `data_analyst → supervisor` → devuelve resultados, supervisor decide siguiente paso
4. `supervisor → campaign_strategy` → recomienda y simula campañas
5. `supervisor → insight_narrator` → genera la narrativa ejecutiva final
6. `insight_narrator → END` → respuesta lista

El Supervisor siempre decide el siguiente agente. Los workers siempre vuelven al Supervisor. Insight Narrator siempre es el último.

---

## Los 7 agentes del sistema

| Agente | Especialidad | Herramientas |
|---|---|---|
| **Supervisor** | Clasifica intención y enruta entre agentes | Ninguna (razonamiento puro) |
| **Data Analyst** | KPIs, revenue, segmentos, tendencias | get_dashboard_summary, compute_segment_stats, get_revenue_trend |
| **SQL/Pandas Agent** | Consultas dinámicas sobre el dataset | run_pandas_query, get_rfm_distribution |
| **RAG Knowledge** | Recupera mejores prácticas de marketing | retrieve_marketing_knowledge |
| **Campaign Strategy** | Recomienda campañas, simula ROI | rank_segments, simulate_campaign, get_recommendations |
| **Forecasting** | Predice revenue, churn y LTV | forecast_revenue, predict_churn_risk, estimate_ltv |
| **Insight Narrator** | Convierte todo en narrativa ejecutiva | Ninguna (síntesis de outputs) |

---

## ¿Qué es RAG en este proyecto?

RAG (Retrieval-Augmented Generation) permite que los agentes consulten una **base de conocimiento documental** antes de responder.

```
Documentos de marketing (PDF, Markdown, TXT)
          │
          ▼  Carga y troceo (512 tokens, 64 de solapamiento)
Fragmentos de texto
          │
          ▼  Embeddings: nomic-embed-text (Ollama) o text-embedding-3-small (OpenAI)
Vectores de 768 o 1536 dimensiones
          │
          ▼  Almacenamiento en Qdrant (base de datos vectorial)
Colección: marketing_knowledge
          │
          ▼  Búsqueda por similitud semántica (top-5, score ≥ 0.5)
Documentos relevantes con citas de fuente
          │
          ▼  El agente RAG los incluye en su razonamiento
Respuesta fundamentada en conocimiento real
```

**Documentos incluidos** (en `backend/app/ai/rag/docs/`):
- `estrategia_rfm.md` — Metodología RFM completa
- `retencion_clientes_ecommerce.md` — Estrategias de retención y métricas
- `campanas_crm.md` — Tipos de campañas y mejores prácticas
- `segmentos_marketing.md` — Los 7 segmentos con caracterización detallada
- `playbook_recuperacion_clientes.md` — Estrategias win-back y secuencias de recuperación

---

## ¿Cómo usar Ollama (gratis, sin API key)?

Ollama permite ejecutar modelos LLM localmente en tu máquina, sin coste ni límites.

**Modelos necesarios**:
- `llama3.1:8b` — Modelo principal para razonamiento (~4.7 GB)
- `nomic-embed-text` — Modelo de embeddings para RAG (~274 MB)

**Ventajas de Ollama**:
- ✅ Completamente gratuito
- ✅ Sin límite de peticiones
- ✅ Privacidad total (los datos no salen de tu máquina)
- ✅ Funciona sin internet una vez descargados los modelos

**Limitaciones vs. OpenAI**:
- Respuestas algo más lentas (depende de tu hardware)
- La calidad puede ser inferior en preguntas muy complejas
- Requiere al menos 8 GB de RAM (16 GB recomendado)

---

## Instalación y configuración

### Requisitos previos
- Python 3.11 o superior
- Node.js 18 o superior
- Docker Desktop
- Ollama instalado desde [ollama.com](https://ollama.com)

### 1. Clonar y configurar entorno

```powershell
# Instalar dependencias del backend
cd backend
pip install -r requirements.txt

# Copiar configuración de entorno
copy .env.example .env
```

### 2. Editar el archivo `.env`

Abre `.env` y configura según el proveedor que vayas a usar:

**Para usar Ollama (gratuito, recomendado para empezar)**:
```env
LLM_PROVIDER=ollama
EMBEDDING_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
OLLAMA_EMBEDDING_MODEL=nomic-embed-text
```

**Para usar OpenAI**:
```env
LLM_PROVIDER=openai
EMBEDDING_PROVIDER=openai
OPENAI_API_KEY=sk-tu-clave-aqui
OPENAI_MODEL=gpt-4o-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
```

**Para probar sin modelos (modo mock)**:
```env
LLM_PROVIDER=mock
EMBEDDING_PROVIDER=mock
```

### 3. Instalar y configurar Ollama

```powershell
# Descarga Ollama desde: https://ollama.com
# Luego descarga los modelos necesarios:

ollama pull llama3.1:8b        # ~4.7 GB — modelo principal de razonamiento
ollama pull nomic-embed-text   # ~274 MB — embeddings para RAG

# Verificar que Ollama está corriendo:
ollama list
```

### 4. Lanzar Qdrant (base de datos vectorial)

```powershell
docker run -p 6333:6333 qdrant/qdrant
```

Qdrant quedará disponible en `http://localhost:6333`

### 5. Iniciar el backend

```powershell
cd backend
uvicorn app.main:app --reload --port 8000
```

API disponible en `http://localhost:8000`
Documentación Swagger: `http://localhost:8000/docs`

### 6. Ingestar la base de conocimiento RAG

Antes de hacer consultas que usen RAG, ingesta los documentos:

```powershell
# Con Invoke-RestMethod (PowerShell):
Invoke-RestMethod -Method Post http://localhost:8000/ai/rag/ingest

# O con curl:
curl -X POST http://localhost:8000/ai/rag/ingest
```

Salida esperada:
```json
{
  "status": "success",
  "files": [
    {"file": "estrategia_rfm.md", "chunks": 24},
    {"file": "retencion_clientes_ecommerce.md", "chunks": 31},
    ...
  ],
  "total_chunks": 128
}
```

### 7. Primera consulta al sistema multiagente

```powershell
Invoke-RestMethod `
  -Method Post `
  -Uri "http://localhost:8000/ai/query" `
  -ContentType "application/json" `
  -Body '{"query":"¿Qué segmento de clientes deberíamos priorizar este mes?"}'
```

### 8. Frontend (dashboard)

```powershell
cd frontend
npm install
npm run dev
```

Dashboard disponible en `http://localhost:3000`

---

## Modo Mock — probar sin modelos

El modo mock permite probar toda la arquitectura sin Ollama ni OpenAI:

```env
LLM_PROVIDER=mock
EMBEDDING_PROVIDER=mock
```

En este modo:
- Los agentes devuelven respuestas predefinidas de demostración
- El pipeline completo se ejecuta (supervisor → agentes → narrator)
- No se realizan llamadas externas
- Ideal para desarrollo frontend o testing del pipeline

No se necesita Qdrant activo cuando `EMBEDDING_PROVIDER=mock` (si falla, el RAG devuelve error gracioso sin romper el flujo).

---

## Cambiar de proveedor en tiempo de ejecución

Solo cambia el `.env` y reinicia el servidor:

```powershell
# .env para Ollama (local, gratuito)
LLM_PROVIDER=ollama
EMBEDDING_PROVIDER=ollama

# .env para OpenAI (nube, alta calidad)
LLM_PROVIDER=openai
EMBEDDING_PROVIDER=openai
OPENAI_API_KEY=sk-...

# .env para Mock (desarrollo, sin modelos)
LLM_PROVIDER=mock
EMBEDDING_PROVIDER=mock
```

⚠️ **Nota importante sobre embeddings**: Si cambias `EMBEDDING_PROVIDER` de ollama a openai (o viceversa), las dimensiones de los vectores son diferentes (768 vs 1536). Necesitas **borrar la colección de Qdrant** y volver a ingestar los documentos.

---

## Referencia de endpoints de la API

### Endpoints de IA (nuevos)

| Método | Endpoint | Descripción |
|---|---|---|
| `POST` | `/ai/query` | Consulta en lenguaje natural al sistema multiagente |
| `POST` | `/ai/report` | Genera un informe estructurado (executive/segment/campaign/forecast) |
| `POST` | `/ai/recommendations` | Recomendaciones de campaña con ROI simulado |
| `GET` | `/ai/conversations/{id}` | Historial de la conversación |
| `GET` | `/ai/traces/{id}` | Traza de ejecución de agentes |
| `DELETE` | `/ai/conversations/{id}` | Limpia la sesión |
| `POST` | `/ai/rag/ingest` | Ingesta documentos en la base de conocimiento |
| `GET` | `/ai/health` | Estado de la capa IA (LLM disponible, RAG activo) |

### Endpoints de analítica (existentes)

| Método | Endpoint | Descripción |
|---|---|---|
| `GET` | `/dashboard/summary` | KPIs generales del negocio |
| `GET` | `/dashboard/revenue` | Serie temporal de revenue mensual |
| `GET` | `/customers` | Lista paginada de clientes con filtros |
| `GET` | `/customers/{id}` | Perfil completo de un cliente |
| `GET` | `/segments` | Resumen de todos los segmentos RFM |
| `GET` | `/campaigns/recommendations` | Playbooks de campaña por segmento |
| `POST` | `/campaigns/simulate` | Simula ROI de una campaña |
| `POST` | `/data/upload` | Carga un nuevo dataset |
| `POST` | `/data/retrain` | Reentrena el pipeline ML |

---

## Estructura del proyecto

```
marketing-ia/
├── backend/
│   ├── app/
│   │   ├── api/              Endpoints analíticos existentes
│   │   ├── ml/               Pipeline RFM + clustering
│   │   ├── services/         Servicios de datos y simulación
│   │   └── ai/               Capa multiagente de IA
│   │       ├── config.py     Configuración centralizada
│   │       ├── llm_factory.py  ← Fábrica de LLM y Embeddings (CLAVE)
│   │       ├── agents/       7 agentes especializados
│   │       ├── graph/        Grafo LangGraph (state, builder, executor)
│   │       ├── rag/          Pipeline RAG (Qdrant + embeddings)
│   │       │   └── docs/     Documentos de conocimiento de marketing
│   │       ├── tools/        Herramientas reutilizables por agentes
│   │       ├── memory/       Gestión de sesiones de conversación
│   │       ├── schemas/      Modelos Pydantic de request/response
│   │       ├── services/     Orquestación FastAPI ↔ LangGraph
│   │       └── api/          Rutas FastAPI de la capa IA
│   ├── requirements.txt
│   └── .env.example
├── frontend/                 Dashboard Next.js
├── notebooks/                Análisis exploratorio Jupyter
└── docs/                     Documentación adicional
```

---

## Arquitectura técnica

```
┌──────────────────────────────────────────────────────────────┐
│                        FASTAPI v2.0                           │
│  /dashboard  /customers  /segments  /campaigns  /ai/*         │
└───────────────────────────┬──────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────┐
│               MOTOR MULTIAGENTE LANGGRAPH                     │
│                                                              │
│  AgentState (estado compartido TypedDict)                    │
│       │                                                      │
│  Supervisor ──(Command)──► Data Analyst                      │
│       ◄──────────────────── │                               │
│       │                                                      │
│  Supervisor ──(Command)──► RAG Knowledge ──► Qdrant         │
│       ◄──────────────────── │                               │
│       │                                                      │
│  Supervisor ──(Command)──► Campaign Strategy                │
│       ◄──────────────────── │                               │
│       │                                                      │
│  Supervisor ──(Command)──► Insight Narrator ──► END         │
└──────────────────────────────────────────────────────────────┘
          │                              │
          ▼                              ▼
┌─────────────────┐          ┌─────────────────────┐
│  LLM PROVIDER   │          │   QDRANT (RAG)       │
│                 │          │                       │
│  ollama ─────── │          │  marketing_knowledge  │
│  openai ─────── │          │  768 dim (Ollama)     │
│  mock ─────────  │          │  1536 dim (OpenAI)   │
└─────────────────┘          └─────────────────────┘
```

---

## Por qué es enterprise-grade

| Propiedad | Implementación |
|---|---|
| **Modularidad** | Un archivo por agente, una responsabilidad por módulo |
| **Flexibilidad** | Cambio de proveedor LLM sin tocar código (solo .env) |
| **Extensibilidad** | Nuevo agente = 1 archivo + 1 línea en builder.py |
| **Observabilidad** | Traza completa por query: agente, herramienta, duración |
| **Seguridad** | Límite de iteraciones (12), aislamiento de errores por agente |
| **Memoria** | Sesiones thread-safe, preparadas para Redis/Postgres |
| **Tipos** | TypedDict de estado end-to-end, Pydantic v2 estricto |
| **Async** | Ejecución del grafo completamente asíncrona (`ainvoke`) |
| **Configuración** | pydantic-settings + .env, sin secretos hardcodeados |
| **Sin vendor lock-in** | Soporta OpenAI, Ollama o cualquier proveedor LangChain |

---

## Roadmap

### Fase 2 — Memoria y Persistencia
- Sesiones de conversación en Redis para escalado horizontal
- Historial de conversaciones en PostgreSQL
- LangGraph `checkpointer` para workflows multi-turno persistentes

### Fase 3 — IA Avanzada
- Streaming de respuestas en tiempo real via SSE
- Human-in-the-loop para decisiones de alto impacto
- Evaluación automática de agentes con ground truth
- Integración LangSmith para trazabilidad completa

### Fase 4 — Producción
- Docker Compose completo (API + Qdrant + Redis)
- Manifiestos Kubernetes para despliegue en nube
- Autenticación y rate limiting en endpoints `/ai`
- Stack de observabilidad: Prometheus + Grafana

---

## Stack tecnológico

**Backend:** Python 3.11+ · FastAPI · Pydantic v2 · Pandas · Scikit-learn

**IA/ML:** LangGraph 1.x · LangChain 1.x · Ollama (local) · OpenAI (nube)

**RAG:** Qdrant · nomic-embed-text (Ollama) / text-embedding-3-small (OpenAI)

**Frontend:** Next.js 14 · React 18 · TypeScript · Recharts · Lucide

**Infraestructura:** Docker · Uvicorn · (Redis · Postgres — roadmap)

---

## Resolución de problemas frecuentes

**El servidor da error al iniciar con Ollama**
→ Verifica que Ollama está corriendo: `ollama list`
→ Comprueba que los modelos están descargados: `ollama pull llama3.1:8b`

**RAG no encuentra documentos relevantes**
→ Verifica que Qdrant está activo: `http://localhost:6333`
→ Re-ingesta los documentos: `POST /ai/rag/ingest`
→ Prueba a bajar `RAG_SCORE_THRESHOLD` a 0.3–0.4 en el `.env`

**Las respuestas son lentas con Ollama**
→ Normal en máquinas con CPU. llama3.1:8b requiere ~8 GB RAM.
→ Considera llama3.2:3b para máquinas menos potentes (más rápido, menor calidad)

**Error al cambiar de Ollama a OpenAI con Qdrant**
→ Borra la colección en Qdrant y re-ingesta: las dimensiones de embeddings son diferentes (768 vs 1536)

---

*Proyecto de portfolio que demuestra skills de AI Engineering: orquestación multiagente con LangGraph, pipeline RAG en producción, arquitectura limpia y valor de negocio real.*

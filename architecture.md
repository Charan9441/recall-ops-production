# Architecture --- Recall-Ops

## 1. System Architecture Overview

Recall-Ops is an AI-powered Production Incident Intelligence and Response Agent built around **Hindsight** as the central persistent memory system.

```text
React Dashboard (Vite + TS)
         │
         │ REST API
         ▼
FastAPI Backend (app/main.py)
         │
         ├──────────────────────────┐
         ▼                          ▼
Hindsight Memory Bank          Groq LLM
(recall-ops-production)   (openai/gpt-oss-120b)
         │                          │
  • recall_incidents         • incident reasoning
  • retain_incident          • root cause diagnosis
                             • action recommendations
```

---

## 2. Core Learning Loop Architecture

```text
               NEW INCIDENT TELEMETRY
                         │
                         ▼
             HINDSIGHT MEMORY RECALL
    (Searches historical incident experiences)
                         │
                         ▼
        RELEVANT HISTORICAL MEMORIES RETRIEVED
                         │
                         ▼
          GROQ LLM (openai/gpt-oss-120b)
    (Synthesizes telemetry + recalled memories)
                         │
                         ▼
         ACTIONABLE AI DIAGNOSIS & ACTIONS
                         │
                         ▼
             ENGINEER RESOLVES INCIDENT
                         │
                         ▼
             HINDSIGHT MEMORY RETAIN
     (Stores new root cause & resolution fix)
                         │
                         ▼
        ACCUMULATED ORGANIZATIONAL KNOWLEDGE
```

---

## 3. Backend Module Design

```text
backend/
├── app/
│   ├── main.py                # FastAPI app with CORS & health routes
│   ├── config.py              # Environment configuration loader
│   ├── models.py              # Pydantic schemas (IncidentRequest, ResolutionRequest)
│   ├── routes/
│   │   └── incidents.py       # API endpoints (/api/incidents/analyze, /resolve, /history)
│   └── services/
│       ├── hindsight_service.py # Hindsight SDK wrapper (arecall, aretain)
│       ├── llm_service.py       # Groq SDK integration (openai/gpt-oss-120b)
│       └── incident_service.py  # Orchestrates Recall -> LLM -> Retain workflow
├── data/
│   └── incidents.json         # 10 realistic synthetic operational incidents
├── seed_data.py               # Memory bank seeding script
├── test_memory_learning.py    # Semantic memory retrieval test suite
├── test_learning_loop.py      # End-to-end learning loop verification script
└── test_backend_api.py        # FastAPI endpoints test suite
```

---

## 4. API Boundaries & Data Models

### `POST /api/incidents/analyze`
- **Input**: `IncidentRequest` (`service`, `severity`, `error`, `logs`, `deployment_version`)
- **Processing**:
  1. Construct semantic search query from telemetry.
  2. Call `hindsight_service.recall_incidents(query)` on bank `recall-ops-production`.
  3. Format retrieved memories into system prompt context.
  4. Call `llm_service.analyze_incident(incident, memories)` using Groq `openai/gpt-oss-120b`.
- **Output**: `{ "success": true, "incident": {...}, "analysis": {...}, "memories": [...] }`

### `POST /api/incidents/resolve`
- **Input**: `ResolutionRequest` (`incident_id`, `service`, `error`, `root_cause`, `resolution`, `outcome`, `resolution_time`)
- **Processing**:
  1. Construct rich structured experience memory string.
  2. Call `hindsight_service.retain_incident(content, context)` to store experience in Hindsight.
- **Output**: `{ "success": true, "message": "Incident resolution stored in Hindsight." }`

### `GET /api/incidents/history`
- **Output**: `{ "success": true, "memories": [...] }`

---

## 5. Security & Secret Protection

- All API keys (`GROQ_API_KEY`, `HINDSIGHT_API_KEY`) remain strictly on the backend.
- `.env` files are excluded from Git via `.gitignore`.
- `.env.example` provides safe public configuration guidance.

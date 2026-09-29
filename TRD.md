# TRD --- Recall-Ops

## 1. Technical Overview

Recall-Ops is a web application composed of:

``` text
React + Vite + TypeScript + Tailwind
                    ↓
              FastAPI Backend
                    ↓
        ┌───────────┴───────────┐
        ↓                       ↓
   Hindsight                  Groq
   Memory API                  LLM
```

The backend is responsible for orchestration. The frontend never
directly accesses Hindsight or LLM credentials.

------------------------------------------------------------------------

# 2. Technology Stack

## Frontend

-   React
-   Vite
-   TypeScript
-   Tailwind CSS
-   Fetch API or Axios

## Backend

-   Python 3.11+
-   FastAPI
-   Pydantic
-   Uvicorn

## AI

-   Groq API
-   Hackathon-supported LLM

The official hackathon material recommends Groq for fast inference and
identifies `openai/gpt-oss-120b` and `qwen/qwen3-32b` as recommended
models. The exact available model should be verified at implementation
time. fileciteturn0file0L39-L44

## Memory

-   Hindsight Cloud or Hindsight self-hosted
-   `hindsight-client`

Current Hindsight documentation provides Python and TypeScript clients
and supports `retain`, `recall`, and `reflect`. citeturn0search3

------------------------------------------------------------------------

# 3. Runtime Architecture

``` text
Browser
   │
   │ HTTP/JSON
   ▼
React Frontend
   │
   │ REST API
   ▼
FastAPI Backend
   │
   ├──────────────► Hindsight
   │                  │
   │                  ├── retain
   │                  ├── recall
   │                  └── reflect (optional)
   │
   └──────────────► Groq LLM
```

------------------------------------------------------------------------

# 4. Backend Modules

Recommended structure:

``` text
backend/
└── app/
    ├── main.py
    ├── config.py
    ├── models.py
    ├── routes/
    │   └── incidents.py
    ├── services/
    │   ├── hindsight_service.py
    │   ├── llm_service.py
    │   └── incident_service.py
    └── prompts/
        └── incident_agent.txt
```

------------------------------------------------------------------------

# 5. Configuration

Environment variables:

``` env
GROQ_API_KEY=
GROQ_MODEL=

HINDSIGHT_BASE_URL=
HINDSIGHT_API_KEY=
HINDSIGHT_BANK_ID=recall-ops-production
```

Never expose these values to the frontend.

------------------------------------------------------------------------

# 6. Hindsight Client

Use the official Hindsight client.

Conceptual Python setup:

``` python
from hindsight_client import Hindsight

client = Hindsight(
    base_url=settings.hindsight_base_url,
    api_key=settings.hindsight_api_key,
)
```

The exact constructor/configuration should follow the current installed
SDK version.

------------------------------------------------------------------------

# 7. Hindsight Operations

## 7.1 Retain

Use retain after a resolution is recorded.

Conceptual:

``` python
client.retain(
    bank_id=bank_id,
    content=incident_memory
)
```

Hindsight retain processes content, extracts structured memories and
indexes them for retrieval. citeturn0search6

### Retain content should include

``` text
Incident ID
Service
Severity
Error
Logs
Version
Symptoms
Root cause
Resolution
Outcome
Resolution time
Timestamp
```

------------------------------------------------------------------------

# 8. Recall

Use recall when analyzing a new incident.

Conceptual:

``` python
result = client.recall(
    bank_id=bank_id,
    query=query
)
```

Hindsight's recall operation searches memory using multiple retrieval
strategies and returns relevant memories. Current documentation
describes semantic, keyword, graph and temporal retrieval.
citeturn0search0turn0search5

### Query construction

Build a compact query from:

``` text
service
error
important log symptoms
deployment version
```

Example:

``` text
payment-api HTTP 503 connection pool exhausted
payment-service v2.4.1
```

Do not put the entire UI state into the query if it adds noise.

------------------------------------------------------------------------

# 9. Reflect

Reflect is an optional second-stage capability.

Conceptual:

``` python
response = client.reflect(
    bank_id=bank_id,
    query=incident_question,
    budget="mid"
)
```

Current Hindsight documentation describes reflect as agentic reasoning
over memory and notes that it can return supporting memories.
citeturn0search2turn0search7

### MVP decision

Start with:

``` text
recall → Groq
```

because it provides maximum control over:

-   evidence
-   prompt
-   output schema
-   UI memory display

Add:

``` text
reflect
```

only after the base flow is stable.

------------------------------------------------------------------------

# 10. Data Models

## IncidentCreate

``` python
class IncidentCreate(BaseModel):
    service: str
    severity: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    error: str
    logs: str
    version: str | None = None
```

## IncidentAnalysis

``` python
class IncidentAnalysis(BaseModel):
    summary: str
    likely_root_cause: str
    recommended_actions: list[str]
    historical_evidence: list[str]
    reasoning: str
```

## IncidentResolution

``` python
class IncidentResolution(BaseModel):
    incident_id: str
    root_cause: str
    resolution: str
    outcome: str
    resolution_time_minutes: int | None = None
```

------------------------------------------------------------------------

# 11. API Specification

## POST `/api/incidents/analyze`

### Request

``` json
{
  "service": "payment-api",
  "severity": "HIGH",
  "error": "HTTP 503",
  "logs": "connection pool exhausted",
  "version": "2.4.1"
}
```

### Processing

``` text
validate
  ↓
create incident ID
  ↓
build memory query
  ↓
Hindsight recall
  ↓
build LLM prompt
  ↓
Groq
  ↓
validate structured response
  ↓
return result
```

### Response

``` json
{
  "incident_id": "INC-1050",
  "analysis": {
    "summary": "Payment API is returning HTTP 503...",
    "likely_root_cause": "Possible connection leak...",
    "recommended_actions": [
      "Inspect DB connection usage",
      "Compare current deployment with v2.4.1",
      "Consider rollback if the same pattern is confirmed"
    ],
    "historical_evidence": [
      "INC-1042 experienced HTTP 503 and connection pool exhaustion",
      "INC-1042 was associated with payment-service v2.4.1"
    ],
    "reasoning": "The current symptoms overlap with the historical incident..."
  },
  "memory_matches": []
}
```

------------------------------------------------------------------------

# 12. POST `/api/incidents/resolve`

### Request

``` json
{
  "incident_id": "INC-1050",
  "root_cause": "Connection leak",
  "resolution": "Rollback to v2.4.0",
  "outcome": "Resolved",
  "resolution_time_minutes": 11
}
```

### Processing

``` text
validate
  ↓
combine current incident + resolution
  ↓
build memory document
  ↓
Hindsight retain
  ↓
return success
```

### Response

``` json
{
  "success": true,
  "incident_id": "INC-1050",
  "memory_status": "stored"
}
```

------------------------------------------------------------------------

# 13. GET `/api/incidents/history`

Returns demo/operational incident history.

Example:

``` json
{
  "incidents": [
    {
      "id": "INC-1042",
      "service": "payment-api",
      "error": "HTTP 503",
      "root_cause": "Connection leak",
      "resolution": "Rollback to v2.4.0"
    }
  ]
}
```

------------------------------------------------------------------------

# 14. LLM Prompt Architecture

Use a system prompt plus structured incident context.

## System prompt

``` text
You are Recall-Ops, an AI production incident-response assistant.

Analyze the current production incident using the supplied
historical incident evidence.

Rules:
1. Never invent historical incidents.
2. Treat retrieved historical memories as evidence, not certainty.
3. Separate observed facts from hypotheses.
4. Do not claim two incidents are identical without evidence.
5. Prefer previous successful resolutions when the evidence is relevant.
6. If historical memory is weak or unavailable, say so explicitly.
7. Produce practical investigation and remediation steps.
```

## User prompt

``` text
CURRENT INCIDENT

Service:
{service}

Severity:
{severity}

Error:
{error}

Logs:
{logs}

Deployment:
{version}

HISTORICAL MEMORY

{retrieved_memories}

Generate the incident analysis.
```

------------------------------------------------------------------------

# 15. Structured LLM Output

Prefer structured JSON.

Schema:

``` json
{
  "summary": "string",
  "likely_root_cause": "string",
  "recommended_actions": [
    "string"
  ],
  "historical_evidence": [
    "string"
  ],
  "reasoning": "string"
}
```

The backend must validate the output before sending it to the frontend.

------------------------------------------------------------------------

# 16. Frontend Architecture

``` text
frontend/
└── src/
    ├── components/
    │   ├── Header.tsx
    │   ├── IncidentForm.tsx
    │   ├── AnalysisPanel.tsx
    │   ├── MemoryPanel.tsx
    │   ├── ResolutionForm.tsx
    │   └── IncidentHistory.tsx
    ├── services/
    │   └── api.ts
    ├── types/
    │   └── incident.ts
    ├── App.tsx
    └── main.tsx
```

------------------------------------------------------------------------

# 17. Frontend State

Minimum state:

``` text
incidentForm
analysis
memoryMatches
loading
error
resolution
history
hindsightStatus
```

No global state library is required for the MVP.

React local state/context is sufficient.

------------------------------------------------------------------------

# 18. Frontend Flow

``` text
User enters incident
        ↓
submit
        ↓
loading
        ↓
backend analysis
        ↓
display:
  - root cause
  - historical memories
  - recommended actions
  - reasoning
        ↓
user resolves incident
        ↓
submit resolution
        ↓
Hindsight updated
        ↓
success notification
```

------------------------------------------------------------------------

# 19. Memory UI

The memory panel should explicitly show:

``` text
🧠 HINDSIGHT MEMORY

Historical incident found

INC-1042
Payment API
HTTP 503

Previous root cause:
Connection leak

Previous resolution:
Rollback v2.4.0
```

If no relevant memory:

``` text
🧠 HINDSIGHT MEMORY

No strong historical match found.

The recommendation is based primarily
on the current incident.
```

Never fabricate a match.

------------------------------------------------------------------------

# 20. Error Handling

## Hindsight failure

Return:

``` json
{
  "memory_status": "unavailable"
}
```

Continue with generic LLM analysis.

UI:

``` text
⚠ Historical memory unavailable.
Generic analysis generated.
```

## Groq failure

Display:

``` text
AI analysis temporarily unavailable.
Please retry.
```

## Invalid LLM output

Backend should:

1.  attempt safe parsing
2.  retry once if practical
3.  otherwise return a controlled error

------------------------------------------------------------------------

# 21. Logging

Backend should log:

-   request ID
-   incident ID
-   API operation
-   Hindsight operation success/failure
-   LLM operation success/failure
-   latency

Do not log:

-   API keys
-   credentials
-   secrets
-   sensitive production logs

------------------------------------------------------------------------

# 22. Security

``` text
Browser
   ↓
FastAPI
   ↓
Secrets
```

Never:

``` text
Browser → Hindsight directly
Browser → Groq directly
```

API keys belong only in backend environment variables.

------------------------------------------------------------------------

# 23. CORS

During local development:

``` text
Frontend:
http://localhost:5173

Backend:
http://localhost:8000
```

Configure FastAPI CORS for the frontend origin.

For deployment, restrict CORS to the deployed frontend domain.

------------------------------------------------------------------------

# 24. Environment Setup

Backend:

``` bash
python -m venv .venv
pip install fastapi uvicorn pydantic python-dotenv hindsight-client groq
```

Frontend:

``` bash
npm create vite@latest frontend -- --template react-ts
cd frontend
npm install
npm install -D tailwindcss
```

Exact package setup should follow current package documentation if
commands differ.

------------------------------------------------------------------------

# 25. Seed Data

Create:

``` text
backend/data/incidents.json
```

with at least 6--10 realistic synthetic incidents.

The seed script should retain the incidents into Hindsight.

Example command:

``` bash
python seed_data.py
```

Do not require seed data for production runtime.

------------------------------------------------------------------------

# 26. Testing

## Unit tests

Test:

-   incident validation
-   query construction
-   prompt construction
-   response parsing
-   resolution formatting

## Integration tests

Test:

``` text
API → Hindsight
API → Groq
API → Hindsight + Groq
```

## End-to-end test

``` text
seed incident
    ↓
submit similar incident
    ↓
retrieve historical memory
    ↓
generate recommendation
    ↓
resolve incident
    ↓
retain new memory
    ↓
submit another similar incident
```

------------------------------------------------------------------------

# 27. Performance Strategy

The MVP should prioritize speed.

### Analyze request

Parallelism can be introduced later, but the basic sequence is:

``` text
Hindsight recall
      ↓
LLM generation
```

Use a small/fast LLM model when possible.

Hindsight documentation notes that recall is intended for retrieval and
is lower-cost/lower-latency than reflect, while reflect performs
additional reasoning. citeturn0search10turn0search11

------------------------------------------------------------------------

# 28. Deployment Architecture

Hackathon MVP:

``` text
Browser
   ↓
Vercel / static frontend
   ↓
FastAPI deployment
   ↓
Hindsight Cloud
   ↓
Groq
```

Alternative:

``` text
Docker
 ├── frontend
 ├── backend
 └── Hindsight
```

For the 200-minute hackathon, Hindsight Cloud is preferred if it reduces
setup time.

------------------------------------------------------------------------

# 29. Observability

Minimum:

``` text
request ID
incident ID
Hindsight status
LLM status
latency
```

Future:

-   OpenTelemetry
-   structured logs
-   metrics
-   tracing

------------------------------------------------------------------------

# 30. Technical Risks

  Risk                      Impact   Mitigation
  ------------------------- -------- --------------------------
  Hindsight setup failure   High     Test first
  LLM rate limit            High     Use fast supported model
  Bad retrieval             High     Seed realistic incidents
  Hallucination             High     Evidence-grounded prompt
  UI delay                  Medium   Loading states
  Invalid JSON              Medium   Pydantic validation
  API key leak              High     Backend-only secrets

------------------------------------------------------------------------

# 31. Technical Definition of Done

``` text
[ ] FastAPI starts
[ ] React starts
[ ] Hindsight connection works
[ ] Seed script works
[ ] Retain works
[ ] Recall works
[ ] Incident analysis works
[ ] Resolution retention works
[ ] Error handling works
[ ] Frontend displays memory
[ ] Complete demo works
```

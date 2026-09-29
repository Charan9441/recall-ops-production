# Architecture --- Recall-Ops

## 1. Architecture Overview

Recall-Ops is designed as a lightweight AI-agent application with
Hindsight as the persistent organizational memory layer.

``` text
┌─────────────────────────────────────────────────────────────┐
│                        USER / ENGINEER                      │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                     REACT FRONTEND                          │
│                                                             │
│  Incident Form → Analysis → Memory → Resolution → History  │
└──────────────────────────────┬──────────────────────────────┘
                               │ REST / JSON
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                       FASTAPI BACKEND                        │
│                                                             │
│  Routes → Incident Service → AI/Memory Services             │
└──────────────┬──────────────────────────────┬───────────────┘
               │                              │
               ▼                              ▼
┌──────────────────────────┐       ┌──────────────────────────┐
│       HINDSIGHT          │       │        GROQ LLM          │
│                          │       │                          │
│ retain                   │       │ Incident reasoning       │
│ recall                   │       │ Structured output        │
│ reflect (optional)       │       │                          │
│                          │       │                          │
│ Organizational Memory    │       │ Agent Reasoning          │
└──────────────────────────┘       └──────────────────────────┘
```

Hindsight's current documentation defines `retain`, `recall`, and
`reflect` as the main memory operations: retain stores information,
recall retrieves relevant memories, and reflect reasons over memories to
produce a synthesized answer. citeturn0search0

------------------------------------------------------------------------

# 2. Architectural Principles

## Principle 1 --- Memory First

Hindsight is not an add-on.

The core product loop is:

``` text
Experience
   ↓
Memory
   ↓
Retrieval
   ↓
Reasoning
   ↓
Action
   ↓
New Experience
```

## Principle 2 --- Evidence Before Recommendation

The agent should retrieve historical evidence before producing its final
recommendation.

## Principle 3 --- Human-in-the-Loop

The MVP recommends actions.

It does not automatically execute dangerous production remediation.

## Principle 4 --- Explicit Memory Visibility

The UI should expose historical evidence so judges can see that
Hindsight actually matters.

## Principle 5 --- Simple MVP

One workflow should work extremely well before additional integrations
are added.

------------------------------------------------------------------------

# 3. High-Level Component Architecture

``` text
                        ┌───────────────┐
                        │    Browser    │
                        └───────┬───────┘
                                │
                                ▼
                        ┌───────────────┐
                        │ React / Vite  │
                        └───────┬───────┘
                                │
                             REST API
                                │
                                ▼
                    ┌───────────────────────┐
                    │       FastAPI         │
                    │                       │
                    │  Incident Controller  │
                    └───────────┬───────────┘
                                │
              ┌─────────────────┼─────────────────┐
              │                 │                 │
              ▼                 ▼                 ▼
      ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
      │ Incident     │  │ Hindsight    │  │ LLM Service  │
      │ Service      │  │ Service      │  │              │
      └──────────────┘  └──────┬───────┘  └──────┬───────┘
                               │                 │
                               ▼                 ▼
                         Hindsight API       Groq API
```

------------------------------------------------------------------------

# 4. Frontend Architecture

``` text
src/
├── components/
│   ├── Header
│   ├── IncidentForm
│   ├── AnalysisPanel
│   ├── MemoryPanel
│   ├── RecommendationPanel
│   ├── ResolutionForm
│   └── IncidentHistory
│
├── services/
│   └── api.ts
│
├── types/
│   └── incident.ts
│
├── App.tsx
└── main.tsx
```

## Responsibilities

### IncidentForm

Collects:

-   service
-   severity
-   error
-   logs
-   version

### AnalysisPanel

Displays:

-   incident summary
-   root cause
-   reasoning

### MemoryPanel

Displays:

-   historical incidents
-   relevant facts
-   Hindsight status

### RecommendationPanel

Displays:

-   recommended actions

### ResolutionForm

Collects:

-   root cause
-   resolution
-   outcome
-   resolution time

### IncidentHistory

Displays prior incidents.

------------------------------------------------------------------------

# 5. Backend Architecture

``` text
app/
├── main.py
├── config.py
├── models.py
│
├── routes/
│   └── incidents.py
│
├── services/
│   ├── incident_service.py
│   ├── hindsight_service.py
│   └── llm_service.py
│
└── prompts/
    └── incident_agent.txt
```

## Layer responsibilities

### Routes

HTTP concerns only:

-   parse request
-   call service
-   return response

### Incident service

Business workflow:

-   create incident
-   normalize data
-   construct retrieval query
-   combine evidence
-   orchestrate analysis

### Hindsight service

Only Hindsight operations:

``` text
retain()
recall()
reflect()
```

### LLM service

Only LLM operations:

``` text
generate_analysis()
```

This separation keeps the code easy to modify.

------------------------------------------------------------------------

# 6. Hindsight Architecture

``` text
                 ┌────────────────────────┐
                 │ recall-ops-production   │
                 │      Memory Bank        │
                 └───────────┬────────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
          ▼                  ▼                  ▼
     World Facts        Experience       Observations
          │                  │                  │
          │                  │                  │
          └──────────────────┴──────────────────┘
                             │
                             ▼
                    Future Retrieval
```

Hindsight currently supports world facts, experience facts and
observations in recall. citeturn0search5

For Recall-Ops, experience memory is particularly important because
incidents and actions are historical events.

------------------------------------------------------------------------

# 7. Memory Lifecycle

## Step 1 --- Incident occurs

``` text
Production incident
```

## Step 2 --- Incident submitted

``` text
React
 ↓
FastAPI
```

## Step 3 --- Search memory

``` text
FastAPI
 ↓
Hindsight recall
 ↓
Historical incidents
```

## Step 4 --- Reason

``` text
Current incident
+
Historical memory
 ↓
Groq
 ↓
Recommendation
```

## Step 5 --- Resolution

Engineer resolves the incident.

## Step 6 --- Learn

``` text
Current incident
+
Actual root cause
+
Resolution
+
Outcome
 ↓
Hindsight retain
```

## Step 7 --- Future use

The new memory becomes available to future incident analysis.

------------------------------------------------------------------------

# 8. Detailed Analyze Sequence

``` text
User
 │
 │ Submit incident
 ▼
React
 │
 │ POST /api/incidents/analyze
 ▼
FastAPI
 │
 ├── Validate
 │
 ├── Generate incident ID
 │
 ├── Build retrieval query
 │
 ▼
Hindsight
 │
 │ recall()
 │
 ▼
Historical Memories
 │
 └────────────────────┐
                      ▼
               LLM Service
                      │
               Current Incident
                      +
               Historical Evidence
                      │
                      ▼
                  Groq LLM
                      │
                      ▼
              Structured Analysis
                      │
                      ▼
                   FastAPI
                      │
                      ▼
                    React
                      │
                      ▼
                    User
```

------------------------------------------------------------------------

# 9. Detailed Resolution Sequence

``` text
User
 │
 │ Submit resolution
 ▼
React
 │
 │ POST /api/incidents/resolve
 ▼
FastAPI
 │
 ├── Validate resolution
 │
 ├── Build incident experience
 │
 ▼
Hindsight
 │
 │ retain()
 │
 ▼
Memory Bank
 │
 │
 ▼
FastAPI
 │
 ▼
React
 │
 ▼
"Memory updated"
```

------------------------------------------------------------------------

# 10. Hindsight vs. LLM Responsibilities

## Hindsight

Responsible for:

-   persistent memory
-   memory extraction
-   retrieval
-   historical evidence
-   accumulated organizational knowledge

## Groq LLM

Responsible for:

-   reasoning
-   synthesis
-   diagnosis
-   recommendation
-   natural-language response

This separation prevents the LLM from being treated as the source of
historical truth.

------------------------------------------------------------------------

# 11. Recommended MVP Analysis Pattern

``` text
Current Incident
       │
       ▼
Hindsight Recall
       │
       ▼
Relevant Historical Evidence
       │
       ├──────────────┐
       │              │
       ▼              ▼
Current Context    Historical Context
       │              │
       └──────┬───────┘
              ▼
          Groq LLM
              │
              ▼
       Structured Result
              │
       ┌──────┼───────┐
       ▼      ▼       ▼
    Cause  Actions  Evidence
```

------------------------------------------------------------------------

# 12. Why Recall Before Groq

The application needs to expose the actual historical evidence used by
the recommendation.

Therefore:

``` text
Hindsight recall
       ↓
display evidence
       ↓
send evidence to LLM
       ↓
generate recommendation
```

This gives the UI a transparent memory section.

Hindsight documentation explicitly distinguishes recall as retrieval and
reflect as synthesized reasoning. citeturn0search10turn0search11

------------------------------------------------------------------------

# 13. Optional Reflect Architecture

After the MVP works:

``` text
Current Incident
       ↓
Hindsight Reflect
       ↓
Hindsight autonomously retrieves memories
       ↓
Reasoning
       ↓
Response + supporting memories
```

Reflect can be useful for deeper incident synthesis. Current
documentation says reflect performs an agentic reasoning loop, retrieves
memories, reasons over them and returns supporting information.
citeturn0search2turn0search7

However, it should not delay the MVP.

------------------------------------------------------------------------

# 14. API Boundary

``` text
Frontend
    │
    │ JSON
    ▼
/api/incidents/analyze
/api/incidents/resolve
/api/incidents/history
```

The frontend should not know:

-   Hindsight API format
-   Groq API format
-   memory bank implementation
-   API keys

This keeps the frontend stable if backend providers change.

------------------------------------------------------------------------

# 15. Failure Architecture

## Hindsight unavailable

``` text
Incident
 ↓
Hindsight error
 ↓
Fallback
 ↓
Generic LLM analysis
 ↓
UI warning
```

The response must say:

``` text
Historical memory was unavailable.
This analysis is based on the current incident only.
```

## LLM unavailable

``` text
Incident
 ↓
LLM error
 ↓
Controlled error response
 ↓
Retry option
```

## Invalid response

``` text
LLM
 ↓
Schema validation
 ↓
Invalid
 ↓
Retry / controlled failure
```

------------------------------------------------------------------------

# 16. Security Architecture

``` text
                     PUBLIC
                        │
                        ▼
                 React Frontend
                        │
                        ▼
                 FastAPI Backend
                  /            \
                 /              \
                ▼                ▼
         Hindsight API        Groq API
          API Key              API Key
             │                   │
             └──── server-side ──┘
```

Secrets never enter the browser bundle.

------------------------------------------------------------------------

# 17. Deployment Architecture

## Recommended hackathon deployment

``` text
                     Internet
                         │
                         ▼
                ┌─────────────────┐
                │ Vercel / Static  │
                │ React Frontend   │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ FastAPI Backend  │
                │ Cloud Deployment │
                └───────┬─┬───────┘
                        │ │
              ┌─────────┘ └─────────┐
              ▼                     ▼
       Hindsight Cloud          Groq API
```

For the time-constrained MVP, Hindsight Cloud is preferred if it avoids
local infrastructure setup.

------------------------------------------------------------------------

# 18. Repository Architecture

``` text
recall-ops/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── models.py
│   │   ├── routes/
│   │   │   └── incidents.py
│   │   ├── services/
│   │   │   ├── incident_service.py
│   │   │   ├── hindsight_service.py
│   │   │   └── llm_service.py
│   │   └── prompts/
│   │       └── incident_agent.txt
│   │
│   ├── data/
│   │   └── incidents.json
│   │
│   ├── seed_data.py
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   ├── types/
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   └── vite.config.ts
│
├── docs/
│   └── demo-script.md
│
├── research.md
├── PRD.md
├── TRD.md
├── architecture.md
├── README.md
└── .gitignore
```

------------------------------------------------------------------------

# 19. Scalability Path

## MVP

``` text
One organization
One memory bank
One FastAPI service
One LLM provider
```

## Future

``` text
                API Gateway
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
   Organization A         Organization B
        │                       │
        ▼                       ▼
   Memory Bank A           Memory Bank B
```

Hindsight supports isolated memory banks, making organization-specific
memory a natural future architecture.

------------------------------------------------------------------------

# 20. Future Integration Architecture

``` text
                    ┌──────────────┐
                    │ PagerDuty    │
                    └──────┬───────┘
                           │
┌──────────────┐           │
│ Slack        │───────────┤
└──────────────┘           │
                           ▼
                    ┌──────────────┐
┌──────────────┐    │ Recall-Ops   │
│ GitHub       │───►│ Ingestion    │
└──────────────┘    └──────┬───────┘
                           ▼
                      Hindsight
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
         Diagnosis      Runbooks     Postmortems
```

------------------------------------------------------------------------

# 21. Architecture Decision Records

## ADR-001 --- Hindsight as primary memory

**Decision:** Use Hindsight as the persistent memory layer.

**Reason:** It is required by the hackathon and directly maps to the
project's central value proposition.

------------------------------------------------------------------------

## ADR-002 --- FastAPI backend

**Decision:** Use FastAPI.

**Reason:** Fast Python API development, straightforward async support,
strong validation through Pydantic, and easy integration with AI SDKs.

------------------------------------------------------------------------

## ADR-003 --- React frontend

**Decision:** Use React + Vite + TypeScript.

**Reason:** Fast development and suitable for a polished single-page
hackathon dashboard.

------------------------------------------------------------------------

## ADR-004 --- Recall before LLM

**Decision:** Use Hindsight recall before generating the final LLM
response.

**Reason:** Gives explicit evidence that can be displayed in the UI and
supplied to the LLM.

------------------------------------------------------------------------

## ADR-005 --- No autonomous remediation

**Decision:** The MVP only recommends actions.

**Reason:** Production remediation can be dangerous and would increase
complexity. Human approval remains in the loop.

------------------------------------------------------------------------

# 22. Final Architecture

``` text
                         RECALL-OPS
                             │
             ┌───────────────┴───────────────┐
             │                               │
             ▼                               ▼
      React Dashboard                  Incident History
             │
             ▼
        FastAPI API
             │
       ┌─────┴─────┐
       │           │
       ▼           ▼
   Hindsight     Groq
       │           │
       │           │
       └─────┬─────┘
             ▼
      Context-Aware AI
       Incident Agent
             │
       ┌─────┴─────┐
       ▼           ▼
 Diagnosis      Actions
       │
       ▼
 Engineer resolves
       │
       ▼
 Hindsight Retain
       │
       ▼
Organizational Memory
       │
       └──────────────► Future Incidents
```

The architecture is intentionally centered on one loop:

> **Incident → Memory → Reasoning → Resolution → Memory**

That loop is the core of Recall-Ops.

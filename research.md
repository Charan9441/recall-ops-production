# RECALL-OPS --- Research & Build Specification

## 1. Project Identity

**Project name:** Recall-Ops\
**Tagline:** Production Incident Intelligence with Persistent Memory\
**Hackathon theme:** AI Agents That Learn Using Hindsight\
**Primary use case:** Production incident response / DevOps\
**Core technology:** Hindsight\
**Target user:** DevOps engineers, SREs, backend engineers, engineering
teams\
**MVP goal:** Build an AI incident-response agent that becomes more
useful as the organization accumulates incident history.

------------------------------------------------------------------------

# 2. Hackathon Requirements

The official HackwithHyderabad 3.0 problem-statement document defines
the hackathon around AI applications using Hindsight, a memory system
designed to let agents remember, recall, and improve over time.

Important requirements:

-   Hindsight is mandatory.
-   The project must clearly demonstrate how Hindsight memory is used.
-   The submission requires a GitHub repository with clean/documented
    code.
-   A demo video is required.
-   A live project demo is required.
-   Content deliverables include an article, social media post, and
    video as described by the official content guide.
-   The project should make memory central to the value proposition
    rather than treating it as a decorative feature.

The official judging weights are:

  Criterion                    Weight
  -------------------------- --------
  Innovation                      30%
  Use of Hindsight Memory         25%
  Technical Implementation        20%
  User Experience                 15%
  Real-world Impact               10%

The official guide also emphasizes a tight scope, realistic data, a
clear before/after memory demonstration, and a demo whose value is
obvious quickly.

Source: HackwithHyderabad 3.0 official problem-statement PDF, especially
pages 2, 4, 8 and 9.

------------------------------------------------------------------------

# 3. Chosen Problem

## Incident Response Agent

### Problem

Production systems repeatedly experience similar incidents:

-   HTTP 5xx errors
-   database connection exhaustion
-   service timeouts
-   failed deployments
-   memory spikes
-   dependency failures
-   authentication failures
-   queue backlogs
-   configuration mistakes
-   infrastructure failures

Engineering teams often have historical knowledge about how these
incidents were solved, but that knowledge is distributed across:

-   previous incidents
-   post-mortems
-   logs
-   tickets
-   deployment notes
-   runbooks
-   team conversations

A conventional LLM can produce a plausible diagnosis, but without
persistent organizational memory it may not know what happened during
the team's previous incidents.

### Proposed solution

Recall-Ops is an AI-powered incident-response agent that remembers
previous incidents and uses those memories when analyzing new incidents.

The agent should remember:

-   incident ID
-   service
-   error
-   logs
-   deployment/version
-   severity
-   symptoms
-   root cause
-   resolution
-   commands/actions taken
-   outcome
-   resolution time
-   whether the fix worked
-   related services
-   relevant deployment versions

When a similar incident occurs later, the agent retrieves relevant
historical memory and uses it to produce a context-aware diagnosis and
recommended response.

------------------------------------------------------------------------

# 4. Why Hindsight Is Central

The project must not look like:

> LLM chatbot + Hindsight somewhere in the backend.

Instead, the core product behavior is:

``` text
Incident
   ↓
Retrieve organizational memory
   ↓
Find similar historical incidents
   ↓
Reason using historical evidence
   ↓
Recommend response
   ↓
Resolve incident
   ↓
Store outcome
   ↓
Future incidents become better informed
```

This creates a visible learning loop:

``` text
Incident 1
   ↓
Resolution
   ↓
Hindsight memory
   ↓
Incident 2
   ↓
Historical context retrieved
   ↓
Better recommendation
   ↓
New resolution
   ↓
More memory
```

The most important demo should therefore show the difference between:

``` text
WITHOUT MEMORY
Generic diagnosis
Multiple possible causes
No organizational context
```

and:

``` text
WITH HINDSIGHT
Historical incident found
Previous root cause found
Previous successful resolution found
Deployment/version relationship found
Specific recommendation generated
```

------------------------------------------------------------------------

# 5. Research: What Hindsight Provides

According to the current official Hindsight documentation, Hindsight is
an agent memory system intended to help agents learn over time rather
than merely remember conversation history.

Its main memory operations are:

## 5.1 Retain

`retain` stores information in a memory bank.

It can accept conversations, documents, facts, and other textual
information.

For Recall-Ops, `retain` should be used after an incident is resolved.

Example conceptual memory:

``` text
Incident INC-1042 occurred on payment-api.

Symptoms:
HTTP 503 responses and database connection pool exhaustion.

Deployment:
payment-service v2.4.1.

Root cause:
A connection leak introduced in v2.4.1.

Resolution:
Rolled back to v2.4.0 and restarted affected instances.

Outcome:
Service recovered in 11 minutes.

The rollback successfully resolved the incident.
```

The important principle is to retain enough context that a future query
can retrieve useful historical information.

## 5.2 Recall

`recall` searches the memory bank for relevant memories.

For Recall-Ops:

``` text
Query:
"payment-api HTTP 503 connection pool exhaustion v2.4.1"
```

The system should retrieve relevant historical incidents.

Recall is appropriate when the application needs the actual relevant
memory items/facts.

## 5.3 Reflect

`reflect` is designed to reason over memories and produce a synthesized
response.

For Recall-Ops, reflect can answer questions such as:

``` text
"What should I do about this payment-api incident based on
our previous incidents and successful resolutions?"
```

This is useful when the application needs a recommendation rather than a
raw list of memories.

### Practical distinction

``` text
retain  → remember this
recall  → find relevant memories
reflect → reason about what those memories imply
```

Official Hindsight documentation describes these as the three core
operations.

------------------------------------------------------------------------

# 6. Hindsight Memory Model Relevant to Recall-Ops

Hindsight documentation describes memory types including:

### World facts

General facts about entities, systems, events and things.

Possible examples:

``` text
payment-api uses PostgreSQL.
payment-service v2.4.1 was deployed on September 20.
```

### Experience facts

Things that happened and actions that were taken.

Examples:

``` text
INC-1042 occurred.
The team rolled back v2.4.1.
The rollback resolved the incident.
```

This category is especially important for incident response.

### Observations

Consolidated knowledge synthesized from accumulated facts.

Possible example:

``` text
Payment API incidents involving connection-pool exhaustion
have previously been associated with payment-service v2.4.1.
```

This can make accumulated experience more useful than simply storing raw
incident transcripts.

------------------------------------------------------------------------

# 7. Memory Banks

Hindsight organizes memory into isolated memory banks.

A memory bank can contain:

-   memories
-   documents
-   entities
-   relationships
-   directives/configuration

For this MVP, use a dedicated bank for the organization's incident
knowledge.

Suggested bank ID:

``` text
recall-ops-production
```

Alternative architecture for a multi-tenant SaaS:

``` text
organization/{organization_id}/incidents
```

For the hackathon MVP, one organization bank is simpler and easier to
demonstrate.

------------------------------------------------------------------------

# 8. Product Workflow

## 8.1 New incident

Engineer enters:

``` json
{
  "service": "payment-api",
  "severity": "HIGH",
  "error": "HTTP 503",
  "logs": "connection pool exhausted",
  "version": "2.4.1"
}
```

## 8.2 Incident normalization

Backend converts the input into a structured incident representation.

Example:

``` json
{
  "service": "payment-api",
  "error_class": "HTTP_503",
  "symptoms": [
    "connection pool exhausted"
  ],
  "deployment_version": "2.4.1",
  "severity": "HIGH"
}
```

## 8.3 Hindsight retrieval

Search the incident memory bank using the important attributes.

Possible query:

``` text
payment-api HTTP 503 connection pool exhausted
payment-service v2.4.1
```

## 8.4 Agent reasoning

The LLM receives:

-   current incident
-   retrieved memories
-   system instructions
-   required response format

It generates:

-   likely root cause
-   matching historical incidents
-   recommended actions
-   confidence/explanation
-   evidence from historical memory

## 8.5 Engineer resolves incident

The engineer can enter the actual:

-   root cause
-   action taken
-   result
-   resolution time

## 8.6 Retain outcome

The complete incident outcome is sent to Hindsight.

That makes the next similar incident more useful.

------------------------------------------------------------------------

# 9. Proposed Architecture

``` text
                         ┌──────────────────────┐
                         │      React UI        │
                         │ Incident Dashboard   │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      FastAPI         │
                         │      Backend         │
                         └──────────┬───────────┘
                                    │
                    ┌───────────────┼────────────────┐
                    │               │                │
                    ▼               ▼                ▼
             ┌────────────┐  ┌────────────┐  ┌─────────────┐
             │ Incident   │  │   Groq /   │  │  Hindsight  │
             │ Processor  │  │    LLM     │  │ Memory Bank │
             └────────────┘  └────────────┘  └──────┬──────┘
                    │               │               │
                    └───────────────┴───────────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ AI Incident Analysis │
                         │ Root Cause           │
                         │ Similar Incidents    │
                         │ Recommended Actions  │
                         └──────────────────────┘
```

------------------------------------------------------------------------

# 10. Recommended Technology Stack

## Frontend

-   React
-   Vite
-   TypeScript
-   Tailwind CSS

Purpose:

-   incident input
-   analysis results
-   memory matches
-   resolution recording
-   incident history

## Backend

-   Python
-   FastAPI
-   Pydantic

Purpose:

-   API endpoints
-   incident validation
-   Hindsight integration
-   LLM integration
-   response formatting

## LLM

Recommended hackathon-friendly approach:

-   Groq API
-   A fast supported model

The official hackathon guide specifically recommends Groq because of its
speed and free-tier availability.

The exact model should be selected based on what is available in the
account at implementation time.

## Memory

-   Hindsight Cloud or self-hosted Hindsight

The hackathon provides Hindsight Cloud and also allows the open-source
version.

------------------------------------------------------------------------

# 11. MVP Features

Only build these for the first version.

## Feature 1 --- Incident Intake

Fields:

-   Service
-   Severity
-   Error
-   Logs
-   Deployment version

## Feature 2 --- AI Analysis

Output:

-   probable root cause
-   recommended actions
-   explanation
-   historical matches

## Feature 3 --- Hindsight Memory

Show:

``` text
🧠 Memory Match

INC-1042
87% relevance

Root cause:
Connection leak

Resolution:
Rollback v2.4.1
```

The exact percentage should only be shown if the implementation has a
defensible relevance/similarity value. Otherwise use labels such as:

``` text
Highly relevant
Relevant
No strong historical match
```

Do not fabricate a numeric similarity score.

## Feature 4 --- Resolve Incident

Form:

``` text
Root cause:
[________________]

Resolution:
[________________]

Outcome:
[ Resolved ]

Resolution time:
[ 11 minutes ]
```

## Feature 5 --- Store Learning

Send the resolved incident to Hindsight.

## Feature 6 --- Incident History

Show previous incidents used in the demo.

------------------------------------------------------------------------

# 12. Data Model

For the MVP, the application can keep the operational UI state
lightweight while Hindsight stores the long-term incident knowledge.

Logical incident schema:

``` text
Incident
├── id
├── timestamp
├── service
├── severity
├── error
├── logs
├── deployment_version
├── symptoms[]
├── root_cause
├── resolution
├── outcome
├── resolution_time
└── status
```

Example:

``` json
{
  "id": "INC-1042",
  "timestamp": "2026-09-25T14:32:00Z",
  "service": "payment-api",
  "severity": "HIGH",
  "error": "HTTP 503",
  "logs": "DB connection pool exhausted",
  "deployment_version": "2.4.1",
  "symptoms": [
    "HTTP 503",
    "database connection exhaustion"
  ],
  "root_cause": "Connection leak",
  "resolution": "Rollback to v2.4.0",
  "outcome": "Resolved",
  "resolution_time": "11 minutes",
  "status": "resolved"
}
```

------------------------------------------------------------------------

# 13. Seed Dataset

The MVP should contain realistic synthetic historical incidents.

Suggested incidents:

## INC-1001 --- Payment API

Service:

``` text
payment-api
```

Error:

``` text
HTTP 503
```

Root cause:

``` text
Database connection exhaustion
```

Resolution:

``` text
Increase connection pool and restart affected instances
```

------------------------------------------------------------------------

## INC-1002 --- Authentication Service

Error:

``` text
JWT validation failures
```

Root cause:

``` text
Signing-key rotation mismatch
```

Resolution:

``` text
Synchronize signing keys and restart authentication instances
```

------------------------------------------------------------------------

## INC-1003 --- Order Service

Error:

``` text
HTTP 502
```

Root cause:

``` text
Upstream service timeout
```

Resolution:

``` text
Fix upstream timeout and retry configuration
```

------------------------------------------------------------------------

## INC-1004 --- Payment API

Error:

``` text
HTTP 503
```

Root cause:

``` text
Connection leak introduced in v2.4.1
```

Resolution:

``` text
Rollback to v2.4.0
```

This incident should become the key demonstration memory.

------------------------------------------------------------------------

## INC-1005 --- Notification Service

Error:

``` text
Message delivery backlog
```

Root cause:

``` text
Consumer throughput reduction
```

Resolution:

``` text
Scale consumers and restore throughput
```

------------------------------------------------------------------------

## INC-1006 --- Search Service

Error:

``` text
High latency
```

Root cause:

``` text
Unoptimized query introduced during deployment
```

Resolution:

``` text
Rollback deployment and optimize query
```

------------------------------------------------------------------------

# 14. Key Demonstration Scenario

This should be the primary demo.

## Phase A --- Existing historical incident

Store:

``` text
INC-1042

Payment API
HTTP 503
Connection pool exhausted
Version 2.4.1

Root cause:
Connection leak

Resolution:
Rollback v2.4.1
```

Retain it in Hindsight.

## Phase B --- New incident

Input:

``` text
Service:
payment-api

Error:
HTTP 503

Logs:
connection pool exhausted

Version:
2.4.1
```

## Phase C --- Memory retrieval

Hindsight retrieves the previous incident.

UI:

``` text
🧠 HISTORICAL MEMORY FOUND

INC-1042

Payment API
HTTP 503
Connection pool exhausted

Previous root cause:
Connection leak

Previous resolution:
Rollback v2.4.1
```

## Phase D --- AI recommendation

``` text
This incident closely matches a previous
payment-api incident.

The previous incident was caused by a
connection leak associated with v2.4.1.

Recommended actions:

1. Inspect connection usage.
2. Compare the current deployment with v2.4.1.
3. Roll back to v2.4.0 if the same leak is confirmed.
```

## Phase E --- Resolve and learn

Engineer records:

``` text
Root cause:
Connection leak

Resolution:
Rollback v2.4.1

Outcome:
Resolved in 11 minutes
```

The agent retains the new experience.

## Phase F --- Repeat

A later incident retrieves both experiences.

This demonstrates cumulative organizational memory.

------------------------------------------------------------------------

# 15. Demo Story

The presentation should tell a simple story:

### Problem

``` text
Production is down.

The engineer has seen this before,
but the knowledge is buried in old incidents.
```

### Traditional AI

``` text
AI generates a generic list of possible causes.
```

### Recall-Ops

``` text
AI searches organizational memory.
```

### Hindsight

``` text
Previous incident found.
Root cause found.
Successful resolution found.
```

### Result

``` text
The agent recommends a response using
the team's own historical experience.
```

### Learning loop

``` text
Every resolved incident becomes future knowledge.
```

------------------------------------------------------------------------

# 16. UI Design

Use one primary dashboard.

## Header

``` text
RECALL-OPS
Production Incident Intelligence

● HINDSIGHT CONNECTED
● AI ONLINE
```

## Main area

Left:

``` text
NEW INCIDENT

Service
Error
Severity
Version
Logs

[ ANALYZE INCIDENT ]
```

Right:

``` text
AI ANALYSIS

Likely Root Cause

Recommended Actions

Historical Evidence
```

## Memory section

``` text
🧠 HINDSIGHT MEMORY

3 relevant historical incidents

INC-1042
Payment API
Connection leak
Rollback v2.4.1
```

## Resolution section

``` text
RESOLVE INCIDENT

Root Cause
Resolution
Outcome
Resolution Time

[ SAVE TO MEMORY ]
```

The UI should make Hindsight visible instead of hiding it in backend
code.

------------------------------------------------------------------------

# 17. API Design

## POST /incident/analyze

Request:

``` json
{
  "service": "payment-api",
  "severity": "high",
  "error": "HTTP 503",
  "logs": "connection pool exhausted",
  "version": "2.4.1"
}
```

Response:

``` json
{
  "incident_id": "INC-1050",
  "analysis": {
    "root_cause": "...",
    "recommended_actions": [],
    "explanation": "..."
  },
  "memory_matches": []
}
```

## POST /incident/resolve

Request:

``` json
{
  "incident_id": "INC-1050",
  "root_cause": "Connection leak",
  "resolution": "Rollback to v2.4.0",
  "outcome": "resolved",
  "resolution_time_minutes": 11
}
```

Backend:

1.  validate data
2.  build incident memory
3.  call Hindsight retain
4.  return success

## GET /incident/history

Returns demonstration/history incidents.

------------------------------------------------------------------------

# 18. Agent Prompt Design

The agent should be instructed to behave as an incident-response
assistant.

Core instructions:

``` text
You are Recall-Ops, an AI production incident-response assistant.

Your job is to analyze a current production incident using:
1. Current incident information.
2. Historical incidents retrieved from Hindsight.

Prioritize evidence from historical incidents when relevant.

Never claim that a historical incident is identical unless
the evidence supports that conclusion.

Separate:
- observed facts
- historical evidence
- likely diagnosis
- recommended actions

Do not invent logs, incidents, resolutions, or historical facts.

When historical memory is weak or absent, explicitly say so.

Return:
1. Summary
2. Historical evidence
3. Likely root cause
4. Recommended actions
5. Confidence/reasoning
```

------------------------------------------------------------------------

# 19. Hindsight Integration Strategy

Recommended first implementation:

``` text
FastAPI
   ↓
Hindsight client
   ↓
retain / recall / reflect
```

### Analyze flow

Option A:

``` text
Current incident
   ↓
Hindsight recall
   ↓
Retrieved memories
   ↓
Groq LLM
   ↓
Structured analysis
```

This gives maximum control over the UI and lets us explicitly show the
retrieved memories.

### Alternative

Use Hindsight `reflect` for the reasoning stage:

``` text
Current incident
   ↓
Hindsight reflect
   ↓
Memory-aware response
```

This can simplify the backend, but explicit `recall` is useful for the
demo because the UI can visibly show which memories were retrieved.

### Recommended MVP

Use:

``` text
retain + recall + LLM
```

and consider `reflect` as an enhancement if the first version is stable.

------------------------------------------------------------------------

# 20. Error Handling

The agent must continue working when memory is unavailable.

Possible states:

``` text
Hindsight connected
```

``` text
Hindsight unavailable
```

If Hindsight fails:

``` text
Memory unavailable.

The agent can still perform a generic
incident analysis, but historical context
could not be retrieved.
```

This is preferable to crashing.

The application should never fabricate a memory match.

------------------------------------------------------------------------

# 21. Security Considerations

For the hackathon MVP:

-   Never hard-code API keys.
-   Use `.env`.
-   Add `.env` to `.gitignore`.
-   Do not expose Hindsight credentials in frontend code.
-   Keep API keys server-side.
-   Avoid using real customer secrets or production credentials in demo
    data.
-   Use synthetic incidents and logs.

Future production version:

-   authentication
-   organization isolation
-   role-based access
-   audit logs
-   encrypted secrets
-   memory deletion/retention policies
-   PII redaction
-   tenant-specific memory banks

------------------------------------------------------------------------

# 22. Real-World Product Potential

A production version could ingest incidents from:

-   PagerDuty
-   Slack
-   Jira
-   GitHub
-   GitHub Actions
-   GitLab CI
-   Datadog
-   Grafana
-   Sentry
-   Kubernetes
-   cloud monitoring systems

Future workflow:

``` text
Monitoring alert
       ↓
Recall-Ops
       ↓
Hindsight memory
       ↓
Similar incidents
       ↓
AI diagnosis
       ↓
Recommended runbook
       ↓
Engineer approval
       ↓
Resolution
       ↓
Automatic post-mortem memory
```

Potential product modules:

1.  Incident intelligence
2.  Post-mortem generation
3.  Runbook recommendation
4.  Deployment-risk analysis
5.  Historical incident search
6.  Team knowledge memory

------------------------------------------------------------------------

# 23. What NOT to Build in MVP

Do not spend hackathon time on:

-   complex authentication
-   multi-tenant billing
-   Kubernetes deployment
-   full observability infrastructure
-   Slack integration
-   PagerDuty integration
-   GitHub integration
-   autonomous production remediation
-   complicated multi-agent systems
-   mobile application
-   elaborate animations
-   large database architecture

The first version should do one workflow extremely well.

------------------------------------------------------------------------

# 24. Technical Risks

## Risk 1 --- Hindsight integration takes too long

Mitigation:

-   Use Hindsight Cloud if available.
-   Test `retain` and `recall` before building the frontend.
-   Keep a minimal Hindsight wrapper in one backend module.

## Risk 2 --- LLM hallucinates

Mitigation:

-   Give it explicit evidence.
-   Tell it not to invent historical incidents.
-   Separate observed facts from hypotheses.
-   Show source memory in the UI.

## Risk 3 --- Demo has no visible learning

Mitigation:

Create the historical incident before the demo.

Then trigger a similar incident.

The second analysis must visibly use the stored memory.

## Risk 4 --- UI consumes too much time

Mitigation:

Build one dashboard.

No complex routing is necessary for the MVP.

------------------------------------------------------------------------

# 25. 200-Minute Build Plan

## 0--20 minutes

Project setup:

``` text
recall-ops/
├── backend/
├── frontend/
├── README.md
├── research.md
└── .env
```

Verify Hindsight connection.

## 20--60 minutes

Build FastAPI backend.

Implement:

``` text
POST /incident/analyze
POST /incident/resolve
GET /incident/history
```

## 60--90 minutes

Implement Hindsight:

``` text
retain
recall
```

Test with seed incidents.

## 90--125 minutes

Build React dashboard.

## 125--150 minutes

Create realistic synthetic incidents.

## 150--170 minutes

Integrate complete learning loop.

## 170--185 minutes

README, architecture and cleanup.

## 185--200 minutes

Demo recording and submission preparation.

------------------------------------------------------------------------

# 26. Definition of Done

The MVP is complete when all of the following work:

### Hindsight

-   [ ] Hindsight is connected.
-   [ ] Historical incident can be retained.
-   [ ] Historical incident can be recalled.
-   [ ] Current incident retrieves relevant history.
-   [ ] Resolved incident is stored again.

### AI

-   [ ] LLM receives current incident.
-   [ ] LLM receives relevant historical evidence.
-   [ ] LLM produces structured diagnosis.
-   [ ] LLM produces recommended actions.
-   [ ] LLM does not invent memory.

### UI

-   [ ] Incident can be entered.
-   [ ] Analysis can be triggered.
-   [ ] Historical memories are visible.
-   [ ] Recommendation is visible.
-   [ ] Incident can be resolved.
-   [ ] Resolution can be saved to memory.

### Demo

-   [ ] Historical incident exists.
-   [ ] Similar new incident is created.
-   [ ] Hindsight retrieves historical evidence.
-   [ ] Agent uses the evidence.
-   [ ] New resolution is stored.
-   [ ] Learning loop is visible.

### Submission

-   [ ] GitHub repository
-   [ ] README
-   [ ] Demo video
-   [ ] Live demo
-   [ ] Hindsight explanation
-   [ ] Required content deliverables

------------------------------------------------------------------------

# 27. Suggested Repository Structure

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
│   │   │   ├── hindsight_service.py
│   │   │   ├── llm_service.py
│   │   │   └── incident_service.py
│   │   └── prompts/
│   │       └── incident_agent.txt
│   ├── seed_data.py
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── types/
│   ├── package.json
│   └── vite.config.ts
│
├── docs/
│   ├── architecture.md
│   └── demo-script.md
│
├── research.md
├── README.md
└── .gitignore
```

------------------------------------------------------------------------

# 28. Future Version

After the hackathon MVP, the product can evolve into an
engineering-memory platform.

Possible architecture:

``` text
                 ┌──────────────────┐
                 │ Monitoring Tools  │
                 └────────┬─────────┘
                          ↓
                 ┌──────────────────┐
                 │  Incident Engine │
                 └────────┬─────────┘
                          ↓
                 ┌──────────────────┐
                 │     Hindsight    │
                 │ Organizational   │
                 │     Memory       │
                 └────────┬─────────┘
                          ↓
             ┌────────────┼────────────┐
             ↓            ↓            ↓
        Diagnosis      Runbooks     Postmortem
             ↓            ↓            ↓
             └────────────┼────────────┘
                          ↓
                 Engineer Decision
                          ↓
                    New Memory
```

The long-term differentiator is not simply "AI analyzes logs."

It is:

> **The agent accumulates organizational incident experience and uses
> that experience to improve future incident response.**

------------------------------------------------------------------------

# 29. Demo Script

## Opening

> "When production goes down, engineers don't just need an AI that can
> reason. They need an AI that remembers what their team already
> learned."

## Problem

> "A normal AI may know common causes of an HTTP 503, but it doesn't
> automatically know that our team saw this exact failure two weeks ago
> and solved it by rolling back a specific deployment."

## Demo

Enter:

``` text
payment-api
HTTP 503
connection pool exhausted
v2.4.1
```

Show Hindsight memory.

> "Recall-Ops searched our historical incident memory and found a
> previous payment-api incident with the same symptoms."

Show:

``` text
Root cause:
Connection leak

Resolution:
Rollback v2.4.1
```

Then:

> "Instead of giving a generic answer, the agent uses our organization's
> own experience to recommend the previous successful resolution."

Save the new resolution.

> "And after this incident is resolved, the outcome becomes memory for
> the next incident."

## Closing

> "Recall-Ops turns incident history into organizational intelligence."

------------------------------------------------------------------------

# 30. Core Product Statement

Use this consistently in the README, pitch and presentation:

> **Recall-Ops is an AI-powered incident response agent that uses
> Hindsight to remember an organization's previous production incidents,
> root causes and successful resolutions, allowing future incidents to
> be analyzed using accumulated operational experience.**

------------------------------------------------------------------------

# 31. One-Sentence Pitch

> **Recall-Ops gives AI agents an engineering team's memory, so every
> production incident makes the next one easier to diagnose.**

------------------------------------------------------------------------

# 32. Research Sources

## Official Hackathon Source

HackwithHyderabad 3.0 --- Problem Statements PDF supplied for this
project.

Key sections: - Hackathon purpose and required technology - Project
selection guidance - Project idea: Incident Response Agent - Demo
guidance - Submission requirements - Judging criteria

## Hindsight Official Documentation

Hindsight main documentation: https://hindsight.vectorize.io/

Quick Start: https://hindsight.vectorize.io/developer/api/quickstart

Main API Methods:
https://hindsight.vectorize.io/developer/api/main-methods

Recall:
https://docs.hindsight.vectorize.io/api-reference/recall-memories/

Reflect: https://hindsight.vectorize.io/developer/api/reflect

Official GitHub: https://github.com/vectorize-io/hindsight

The official Hindsight documentation identifies `retain`, `recall`, and
`reflect` as the core memory operations. It also documents memory types,
memory banks, integrations and deployment options.

------------------------------------------------------------------------

# 33. Important Research Notes

This document distinguishes the hackathon requirements from
implementation decisions.

### Directly required by the hackathon

-   Hindsight must be used.
-   The project must demonstrate Hindsight memory clearly.
-   GitHub repository.
-   Demo video.
-   Live demo.
-   Required content deliverables.
-   Hindsight explanation.

### Product decisions made for this project

-   Incident Response Agent as the selected use case.
-   Recall-Ops as the project name.
-   React + Vite + Tailwind frontend.
-   FastAPI backend.
-   Groq for the LLM.
-   Explicit `retain` + `recall` flow for the MVP.
-   Synthetic production incident dataset.
-   Single-dashboard UX.
-   One primary demo scenario.

These are implementation choices and can be changed if integration
constraints require it.

------------------------------------------------------------------------

# 34. Final Build Principle

The project should always optimize for this experience:

``` text
BEFORE MEMORY

"Here are some possible causes..."

AFTER MEMORY

"We have seen this before.

Here is what happened.
Here is what caused it.
Here is what fixed it.
Here is what we recommend now."
```

That difference is the product.

**Build the memory loop first. Build the UI second. Polish last.**

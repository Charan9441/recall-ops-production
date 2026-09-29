# PRD --- Recall-Ops

## 1. Product Overview

**Product:** Recall-Ops\
**Tagline:** Production Incident Intelligence with Persistent Memory\
**Hackathon:** HackwithHyderabad 3.0 --- AI Agents That Learn Using
Hindsight\
**Primary user:** DevOps engineers, SREs, backend engineers, engineering
teams\
**Product type:** AI-powered incident-response application

### Product statement

Recall-Ops is an AI-powered production incident-response agent that uses
Hindsight to remember previous incidents, root causes, successful
resolutions, and deployment context. When a new incident occurs, the
agent retrieves relevant organizational memory and uses it to produce a
more context-aware diagnosis and response recommendation.

The hackathon problem statement specifically identifies Incident
Response Agent as a target use case and emphasizes remembering past
incidents, root causes, resolution steps, and successful runbooks.
fileciteturn0file0L175-L188

------------------------------------------------------------------------

# 2. Problem Statement

Production incidents are often repetitive.

Engineering teams may encounter the same:

-   service failure
-   HTTP 5xx error
-   database problem
-   deployment regression
-   dependency failure
-   configuration issue
-   latency problem

multiple times.

The team may already have solved a similar incident, but the useful
knowledge is distributed across old incident reports, logs,
post-mortems, tickets, runbooks, and team conversations.

A conventional LLM can reason about the current incident but does not
automatically possess the team's historical experience.

Recall-Ops solves this by turning incident history into persistent
AI-accessible memory.

------------------------------------------------------------------------

# 3. Goals

## Primary goals

1.  Build a working AI incident-response agent.
2.  Make Hindsight the central memory layer.
3.  Demonstrate that historical incidents improve future incident
    analysis.
4.  Provide a clear and fast incident-analysis workflow.
5.  Show the complete learning loop:
    -   incident
    -   analysis
    -   resolution
    -   memory
    -   future retrieval
6.  Produce a polished hackathon-ready MVP.

## Secondary goals

-   Make the project understandable within a 60--90 second demo.
-   Use realistic synthetic incident data.
-   Keep the architecture simple enough to build rapidly.
-   Keep the code modular enough for future integrations.

------------------------------------------------------------------------

# 4. Non-Goals for MVP

The first version will NOT include:

-   full authentication
-   billing
-   multi-tenant SaaS infrastructure
-   real production monitoring
-   autonomous production remediation
-   Kubernetes automation
-   PagerDuty integration
-   Slack integration
-   GitHub integration
-   complex multi-agent orchestration
-   mobile application
-   enterprise RBAC

These may be future extensions.

------------------------------------------------------------------------

# 5. Target Users

## Primary persona --- SRE / DevOps Engineer

Needs to:

-   diagnose incidents quickly
-   understand previous incidents
-   identify recurring failure patterns
-   find successful historical resolutions
-   avoid repeating investigation work

### Pain point

> "I know we've seen something like this before, but finding exactly
> what happened takes too long."

## Secondary persona --- Backend Engineer

Needs:

-   service-level incident context
-   deployment history
-   root-cause clues
-   previous fixes

------------------------------------------------------------------------

# 6. Core User Journey

``` text
Engineer receives incident
        ↓
Opens Recall-Ops
        ↓
Enters incident information
        ↓
AI analyzes current incident
        ↓
Hindsight searches historical memory
        ↓
Relevant incidents are displayed
        ↓
AI produces contextual recommendation
        ↓
Engineer investigates/resolves
        ↓
Engineer records actual root cause + resolution
        ↓
Recall-Ops stores the experience in Hindsight
        ↓
Future incidents can use the new knowledge
```

------------------------------------------------------------------------

# 7. MVP Features

## F1 --- Incident Intake

The user enters:

-   Service
-   Severity
-   Error
-   Logs
-   Deployment version

### Acceptance criteria

-   Required fields are validated.
-   User can submit the incident.
-   Backend receives structured incident data.
-   A unique incident ID is generated.

------------------------------------------------------------------------

## F2 --- AI Incident Analysis

The system analyzes the incident.

Output:

-   summary
-   likely root cause
-   recommended actions
-   reasoning
-   historical evidence

### Acceptance criteria

-   The current incident is included in the LLM prompt.
-   Relevant Hindsight memories are included.
-   The response clearly distinguishes historical evidence from
    hypotheses.
-   The agent does not fabricate historical incidents.

------------------------------------------------------------------------

## F3 --- Hindsight Memory Retrieval

The backend searches the Hindsight memory bank for relevant historical
incidents.

### Acceptance criteria

-   A recall query is generated from the incident.
-   Hindsight is queried before final recommendation generation.
-   Relevant memories are returned to the frontend.
-   The UI identifies that the evidence came from organizational memory.

Hindsight's official documentation defines `recall` as the operation for
searching memory and returning relevant facts, while `reflect`
synthesizes an answer using memories. citeturn0search0turn0search7

------------------------------------------------------------------------

## F4 --- Resolution Recording

After an incident is resolved, the engineer records:

-   Root cause
-   Resolution
-   Outcome
-   Resolution time

### Acceptance criteria

-   Resolution can be submitted.
-   The backend constructs a complete incident experience.
-   The experience is retained in Hindsight.
-   The UI confirms that organizational memory was updated.

------------------------------------------------------------------------

## F5 --- Incident History

Display previously stored/demo incidents.

### Acceptance criteria

-   Historical incidents can be displayed.
-   Important fields are visible.
-   The user can understand why a historical incident was relevant.

------------------------------------------------------------------------

# 8. Hindsight Requirements

Hindsight is mandatory for the hackathon. The official problem statement
explicitly says all teams must build their projects using Hindsight and
that the solution must clearly demonstrate its use.
fileciteturn0file0L27-L35 fileciteturn0file0L317-L328

Recall-Ops will use:

### Retain

Store:

-   incident facts
-   incident experience
-   root cause
-   resolution
-   outcome

### Recall

Retrieve:

-   similar incidents
-   previous root causes
-   previous resolutions
-   deployment relationships

### Reflect

Optional enhancement for the MVP; useful for memory-aware synthesis
directly inside Hindsight.

Hindsight's current documentation describes `retain`, `recall`, and
`reflect` as its three core operations. citeturn0search0

------------------------------------------------------------------------

# 9. Memory Strategy

## Memory bank

Suggested:

``` text
recall-ops-production
```

The bank represents the organization's accumulated incident knowledge.

## Retained memory format

Example:

``` text
Incident ID: INC-1042
Service: payment-api
Severity: HIGH
Error: HTTP 503
Logs: Database connection pool exhausted
Deployment: payment-service v2.4.1

Root cause:
Connection leak introduced in v2.4.1.

Resolution:
Rolled back to v2.4.0 and restarted affected instances.

Outcome:
Resolved in 11 minutes.
```

Hindsight's retain operation processes stored content into structured
memories and indexes them for later retrieval. citeturn0search6

------------------------------------------------------------------------

# 10. Functional Requirements

  ID      Requirement                     Priority
  ------- ------------------------------- ----------
  FR-01   Accept incident information     Must
  FR-02   Validate incident information   Must
  FR-03   Generate incident ID            Must
  FR-04   Query Hindsight                 Must
  FR-05   Display historical evidence     Must
  FR-06   Generate AI analysis            Must
  FR-07   Recommend response actions      Must
  FR-08   Record resolution               Must
  FR-09   Retain resolved incident        Must
  FR-10   Display incident history        Should
  FR-11   Hindsight connection status     Should
  FR-12   Reflect-based reasoning         Could

------------------------------------------------------------------------

# 11. Non-Functional Requirements

## Performance

-   UI should respond quickly.
-   Hindsight recall should not block the entire interface without
    feedback.
-   Loading states must be visible.

## Reliability

If Hindsight is temporarily unavailable, the system should gracefully
fall back to generic incident analysis and explicitly tell the user that
historical memory was unavailable.

## Security

-   API keys remain server-side.
-   Secrets are stored in environment variables.
-   `.env` is excluded from Git.
-   Demo data must not contain real credentials or production secrets.

## Explainability

The application should show:

-   historical evidence
-   why the memory is relevant
-   recommended action
-   distinction between facts and hypotheses

------------------------------------------------------------------------

# 12. User Experience Requirements

The MVP uses one primary dashboard.

### Dashboard sections

1.  Header/status
2.  Incident intake
3.  AI analysis
4.  Hindsight memory
5.  Recommended actions
6.  Resolution recording
7.  Incident history

The UI should make the memory loop visually obvious.

------------------------------------------------------------------------

# 13. Primary Demo Scenario

### Historical incident

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

### New incident

``` text
payment-api
HTTP 503
connection pool exhausted
v2.4.1
```

### Expected behavior

Hindsight retrieves the historical incident.

The AI responds approximately:

``` text
This incident matches a previous payment-api incident.

Historical root cause:
Connection leak associated with v2.4.1.

Previous successful resolution:
Rollback to v2.4.0.

Recommended:
Inspect the connection leak and consider rollback
if the same failure pattern is confirmed.
```

The exact response is generated by the system; this is the expected
product behavior, not a hard-coded answer.

------------------------------------------------------------------------

# 14. Success Metrics

For the hackathon MVP:

### Product success

-   Incident can be submitted end-to-end.
-   Hindsight successfully stores memory.
-   Hindsight successfully retrieves relevant memory.
-   Agent uses retrieved evidence.
-   New resolution is retained.
-   Second similar incident benefits from previous memory.

### Demo success

A judge should understand within one minute:

1.  what the incident problem is
2.  what Recall-Ops does
3.  why Hindsight matters
4.  how the agent improves with memory

------------------------------------------------------------------------

# 15. Future Scope

-   PagerDuty integration
-   Slack incident ingestion
-   GitHub deployment history
-   Sentry integration
-   Grafana/Datadog integration
-   automatic post-mortems
-   runbook recommendation
-   deployment risk detection
-   team-level incident analytics
-   organization-specific memory banks
-   enterprise authentication and RBAC

------------------------------------------------------------------------

# 16. Product Positioning

## One-line pitch

> Recall-Ops gives AI agents an engineering team's memory, so every
> production incident makes the next one easier to diagnose.

## Core differentiator

The system does not merely answer incident questions.

It **accumulates operational experience** and uses that experience
during future incidents.

------------------------------------------------------------------------

# 17. Definition of Done

The MVP is done when:

-   [ ] Hindsight connected
-   [ ] Incident intake works
-   [ ] Hindsight recall works
-   [ ] AI analysis works
-   [ ] Historical memory visible
-   [ ] Resolution form works
-   [ ] Resolved incident retained
-   [ ] Second similar incident retrieves prior knowledge
-   [ ] README completed
-   [ ] Demo scenario works end-to-end
-   [ ] GitHub repository ready

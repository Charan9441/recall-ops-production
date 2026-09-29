# Recall-Ops --- Production Incident Intelligence with Persistent Memory

> **HackwithHyderabad 3.0 Hackathon Submission**  
> *Theme: AI Agents That Learn Using Hindsight*

Recall-Ops is an AI-powered production incident-response agent that uses **Hindsight** as a persistent memory layer to remember past production incidents, root causes, successful fixes, and deployment relationships. When a new incident occurs, Recall-Ops retrieves relevant organizational memory and synthesizes a context-aware diagnosis and recommended remediation.

---

## 🚀 Key Differentiator: The Hindsight Memory Loop

Conventional LLMs reason about incidents using general knowledge, but they lack your team's historical experience. Recall-Ops solves this by establishing a persistent organizational learning loop:

```text
  Production Incident Telemetry
               │
               ▼
   🧠 HINDSIGHT MEMORY RECALL
  (Retrieves historical incidents & past fixes)
               │
               ▼
   🤖 GROQ LLM REASONING (openai/gpt-oss-120b)
  (Synthesizes telemetry with retrieved evidence)
               │
               ▼
   💡 ACTIONABLE RECOMMENDATION & DIAGNOSIS
               │
               ▼
   🔧 ENGINEER RESOLVES INCIDENT
               │
               ▼
   🧠 HINDSIGHT MEMORY RETAIN
  (Stores new root cause & resolution experience)
               │
               ▼
   📈 ACCUMULATED ORGANIZATIONAL KNOWLEDGE
```

---

## 🏗️ Technical Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│                    REACT FRONTEND (Vite + TS)               │
│                                                             │
│  Incident Intake → Memory Panel → Analysis → Resolution    │
└──────────────────────────────┬──────────────────────────────┘
                               │ REST / JSON
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                    FASTAPI BACKEND                          │
│                                                             │
│  Incident Controller → Hindsight Service → LLM Service     │
└──────────────┬──────────────────────────────┬───────────────┘
               │                              │
               ▼                              ▼
┌──────────────────────────┐       ┌──────────────────────────┐
│       HINDSIGHT          │       │        GROQ LLM          │
│       MEMORY API         │       │    openai/gpt-oss-120b   │
│                          │       │                          │
│  • retain (store fix)    │       │  • evidence synthesis    │
│  • recall (search facts) │       │  • root cause diagnosis  │
│  • bank isolation        │       │  • action recommendation │
└──────────────────────────┘       └──────────────────────────┘
```

- **Frontend**: React 18, Vite, TypeScript, Tailwind CSS, Lucide Icons
- **Backend**: Python 3.12, FastAPI, Pydantic v2, Uvicorn
- **Memory Layer**: Hindsight Memory SDK (`hindsight-client`), Bank ID: `recall-ops-production`
- **Inference Engine**: Groq SDK (`openai/gpt-oss-120b`)

---

## 🎯 Demo Scenario (Before vs. After Memory)

### 1. The Incident
`payment-api` throws **HTTP 503** errors with log telemetry `Database connection pool exhausted` on deployment version `v2.4.1`.

### 2. Without Hindsight (Generic AI)
A standard chatbot recommends generic troubleshooting steps: check database server metrics, inspect general network traffic, or scale server hardware.

### 3. With Recall-Ops & Hindsight Memory
Hindsight queries organizational memory and retrieves historical incident **INC-1042**:
- **Historical Root Cause**: Connection leak introduced in `payment-service v2.4.1` pool initialization.
- **Previous Successful Fix**: Rolled back deployment to `v2.4.0` and restarted affected instances (resolved in 11 mins).

Recall-Ops uses this historical evidence to provide a precise, targeted recommendation:
> *"Symptoms match historical incident INC-1042. High probability of connection leak in v2.4.1. Immediately inspect connection handler and execute rollback to v2.4.0."*

### 4. The Learning Loop
When the engineer resolves the incident, Recall-Ops calls Hindsight `retain` to store the experience, making future similar incident diagnoses even smarter.

---

## 🛠️ Quickstart & Setup Guide

### 1. Prerequisites
- Python 3.11+
- Node.js v18+ & npm

### 2. Environment Setup
Copy `.env.example` to `.env` in both project root and `backend/`:

```bash
cp .env.example .env
cp .env.example backend/.env
```

Set your credentials in `.env`:
```env
HINDSIGHT_BASE_URL=https://api.hindsight.vectorize.io
HINDSIGHT_API_KEY=your_hindsight_api_key
HINDSIGHT_BANK_ID=recall-ops-production

GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-120b
```

### 3. Run Backend (FastAPI)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Run backend API server
uvicorn app.main:app --reload --port 8000
```

Verify backend health:
- Root API: `http://localhost:8000/`
- Health check: `http://localhost:8000/health`
- Swagger Docs: `http://localhost:8000/docs`

### 4. Run Automated Backend Verification Tests

```bash
python test_backend_api.py
```

### 5. Run Frontend (React + Vite)

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` in your browser.

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **`GET`** | `/` | Root server status |
| **`GET`** | `/health` | Server health check |
| **`GET`** | `/api/hindsight/status` | Hindsight memory bank connectivity status |
| **`POST`** | `/api/incidents/analyze` | Intake incident, query Hindsight recall, & return AI analysis |
| **`POST`** | `/api/incidents/resolve` | Record resolution & retain experience in Hindsight |
| **`GET`** | `/api/incidents/history` | Retrieve historical memories from Hindsight |

---

## 📁 Repository Structure

```text
recall-ops/
├── backend/
│   ├── app/
│   │   ├── main.py                # FastAPI application entrypoint
│   │   ├── config.py              # Configuration & env loader
│   │   ├── models.py              # Pydantic schemas (IncidentRequest, ResolutionRequest)
│   │   ├── routes/                # REST API routers
│   │   └── services/              # Hindsight & Groq LLM service abstractions
│   ├── data/                      # Synthetic incident dataset
│   ├── seed_data.py               # Memory seeding script
│   └── test_backend_api.py        # Backend verification test suite
├── frontend/
│   ├── src/
│   │   ├── components/            # Header, IncidentForm, MemoryPanel, AnalysisPanel, etc.
│   │   ├── services/              # API client
│   │   ├── types/                 # TypeScript interfaces
│   │   └── App.tsx                # Main incident intelligence dashboard
│   ├── index.html
│   └── vite.config.ts
├── docs/                          # Demo script and guides
├── PRD.md                         # Product Requirements Document
├── TRD.md                         # Technical Requirements Document
├── architecture.md                # System Architecture Specs
└── research.md                    # Research and specification doc
```

---

## ⚖️ Hackathon Evaluation Alignment

| Criterion | Weight | How Recall-Ops Delivers |
| :--- | :---: | :--- |
| **Innovation** | 30% | Transforms scattered incident post-mortems into active, queryable AI agent memory. |
| **Use of Hindsight Memory** | 25% | Hindsight is mandatory for both recall (evidence retrieval) and retain (learning loop). |
| **Technical Implementation** | 20% | FastAPI + Hindsight SDK + Groq `openai/gpt-oss-120b` with fallback architecture. |
| **User Experience** | 15% | Single-screen SRE dashboard making historical memory explicitly visible to judges. |
| **Real-World Impact** | 10% | Reduces mean-time-to-resolution (MTTR) for repetitive production outages. |

---

## 📄 License
MIT License. Built for HackwithHyderabad 3.0.

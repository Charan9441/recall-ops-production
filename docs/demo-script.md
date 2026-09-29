# Recall-Ops --- 90-Second Hackathon Demo Script

> **HackwithHyderabad 3.0 Submission**  
> *Target Duration: 60 - 90 Seconds*

---

## 🎬 Demo Overview & Setup

Before starting the demo:
1. Ensure FastAPI backend is running (`uvicorn app.main:app --port 8000`).
2. Ensure Frontend dashboard is open (`http://localhost:5173`).
3. Click **"Load Primary Demo Incident"** in the top header.

---

## ⏱️ Timeline & Script

### 0:00 - 0:15 | The Problem (Hook)
> *"Production is down! Our `payment-api` is throwing HTTP 503 errors with database connection exhaustion. Engineering teams face repetitive incidents like this all the time. The knowledge of how to fix it exists in old post-mortems or Slack threads, but under outage pressure, finding it takes too long."*

---

### 0:15 - 0:35 | Traditional AI vs. Recall-Ops
> *"If you ask a standard LLM, it gives generic advice: check database metrics, scale server hardware, or check firewall rules. But it has no memory of YOUR engineering team's past experience."*
>
> *"This is **Recall-Ops**, powered by **Hindsight**. When an incident occurs, Recall-Ops doesn't just ask an LLM — it queries Hindsight's persistent memory bank first."*

---

### 0:35 - 0:55 | Hindsight Recall Demonstration
> *"Watch what happens when we submit this incident. In the **🧠 HINDSIGHT MEMORY** panel, Hindsight immediately retrieves historical incident **INC-1042**."*
>
> *"Hindsight shows us that three weeks ago, `payment-api v2.4.1` suffered an identical connection pool leak. The fix was rolling back to `v2.4.0`."*
>
> *"Our AI model, Groq `openai/gpt-oss-120b`, uses this exact historical evidence to produce a context-aware diagnosis: **'High probability of connection leak in v2.4.1 connection pool handler. Recommended Action: Roll back to v2.4.0.'**"*

---

### 0:55 - 1:15 | The Learning Loop (Hindsight Retain)
> *"Now for the most important part: **The Learning Loop**."*
>
> *"Once the SRE confirms the fix and rolls back to `v2.4.0`, they fill in the Resolution form and click **Retain Experience in Hindsight**."*
>
> *"Hindsight processes the root cause and resolution, storing it permanently in the `recall-ops-production` memory bank. Now, every future incident automatically benefits from today's experience."*

---

### 1:15 - 1:30 | Conclusion & Impact
> *"Recall-Ops turns scattered incident history into active organizational memory. With Hindsight, every resolved outage makes the next one faster to diagnose."*
>
> *"Thank you!"*

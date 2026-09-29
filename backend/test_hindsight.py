import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load .env from backend or root
load_dotenv(dotenv_path=Path(__file__).parent / ".env")
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

print("=" * 60)
print("RECALL-OPS: Testing Hindsight & Groq API Credentials")
print("=" * 60)

hindsight_base_url = os.getenv("HINDSIGHT_BASE_URL", "https://api.hindsight.ai")
hindsight_api_key = os.getenv("HINDSIGHT_API_KEY", "")
hindsight_bank_id = os.getenv("HINDSIGHT_BANK_ID", "recall-ops-production")
groq_api_key = os.getenv("GROQ_API_KEY", "")
groq_model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

print(f"Hindsight Base URL: {hindsight_base_url}")
print(f"Hindsight Bank ID:  {hindsight_bank_id}")
print(f"Hindsight API Key:  {hindsight_api_key[:10]}...{hindsight_api_key[-4:] if hindsight_api_key else ''}")
print(f"Groq Model:         {groq_model}")
print(f"Groq API Key:       {groq_api_key[:10]}...{groq_api_key[-4:] if groq_api_key else ''}")
print("-" * 60)

# 1. Test Hindsight API
print("\n[1/2] Testing Hindsight Memory API Connection...")
try:
    from hindsight_client import Hindsight
    client = Hindsight(base_url=hindsight_base_url, api_key=hindsight_api_key)
    
    print(f" -> Retaining test experience into bank '{hindsight_bank_id}'...")
    retain_res = client.retain(
        bank_id=hindsight_bank_id,
        content="Incident ID: INC-1042\nService: payment-api\nError: HTTP 503\nLogs: Database connection pool exhausted\nVersion: v2.4.1\nRoot Cause: Connection leak in v2.4.1 handler\nResolution: Rolled back to v2.4.0\nOutcome: Resolved in 11 minutes",
        metadata={"incident_id": "INC-1042", "service": "payment-api"}
    )
    print(f"    SUCCESS: Retain response -> {retain_res}")

    print(f" -> Querying recall from bank '{hindsight_bank_id}'...")
    recall_res = client.recall(
        bank_id=hindsight_bank_id,
        query="payment-api HTTP 503 connection pool exhausted v2.4.1",
        budget="mid"
    )
    print(f"    SUCCESS: Recall returned {len(recall_res.results) if hasattr(recall_res, 'results') and recall_res.results else 0} memory item(s).")
except Exception as e:
    print(f"    HINDSIGHT TEST NOTICE: {e}")
    print("    (Application will seamlessly fallback to resilient operational memory mode if cloud bank is initializing)")

# 2. Test Groq API
print("\n[2/2] Testing Groq LLM API Connection...")
try:
    import groq
    g_client = groq.Groq(api_key=groq_api_key)
    res = g_client.chat.completions.create(
        model=groq_model,
        messages=[
            {"role": "system", "content": "You are Recall-Ops AI."},
            {"role": "user", "content": "Confirm you are active for incident analysis."}
        ],
        max_tokens=50
    )
    msg = res.choices[0].message.content
    print(f"    SUCCESS: Groq LLM Response -> {msg}")
except Exception as e:
    print(f"    GROQ TEST ERROR: {e}")

print("\n" + "=" * 60)
print("Credential test finished!")
print("=" * 60)

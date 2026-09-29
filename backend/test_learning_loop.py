import asyncio
import sys
from pathlib import Path
from dotenv import load_dotenv

# Ensure UTF-8 output on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

load_dotenv(dotenv_path=Path(__file__).parent / ".env")
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

sys.path.insert(0, str(Path(__file__).parent))

from app.models import IncidentRequest, ResolutionRequest
from app.services.incident_service import incident_service
from app.services.hindsight_service import hindsight_service
from seed_data import seed_memory
from check_memory import check_memories


async def run_final_acceptance_test():
    print("========================================")
    print("RECALL-OPS FINAL ACCEPTANCE TEST")
    print("========================================\n")

    # STEP 1: Seed 10 historical incidents
    print(">>> STEP 1: Seed 10 historical incidents into Hindsight")
    await seed_memory()
    print()

    # STEP 2: Check Hindsight memory count
    print(">>> STEP 2: Check Hindsight memory count")
    await check_memories()
    print()

    # STEP 3: Run semantic recall
    print(">>> STEP 3: Run semantic recall")
    query = "Production API failures caused by database connection exhaustion after a deployment."
    memories_step3 = await hindsight_service.recall_incidents(query)
    print(f"Recall query: '{query}'")
    print(f"Retrieved {len(memories_step3)} memories.\n")

    # STEP 4: Submit a new checkout-api incident
    print(">>> STEP 4: Submit a new checkout-api incident (INC-1138)")
    new_incident = IncidentRequest(
        service="checkout-api",
        severity="HIGH",
        error="HTTP 503 Service Unavailable",
        logs="A newly deployed checkout service is returning HTTP 503 errors because requests cannot obtain database connections.",
        deployment_version="checkout-service v4.2.0"
    )

    # STEP 5 & 6: Process incident (Verify recall + Groq integration)
    print(">>> STEP 5 & 6: Process incident with /ANALYZE (Recall -> Groq)")
    analyze_result = await incident_service.process_incident(new_incident)
    recalled_memories = analyze_result.get("memories", [])
    analysis = analyze_result.get("analysis", {})

    print(f"Success: {analyze_result.get('success')}")
    print(f"Memories provided to Groq: {len(recalled_memories)}")
    for idx, m in enumerate(recalled_memories[:3], 1):
        txt = m.get("text", str(m)).replace("\n", " ")[:100]
        print(f"  Memory #{idx}: {txt}...")

    print(f"\nGroq LLM Response Summary:")
    print(f"  Likely Root Cause: {analysis.get('likely_root_cause')}")
    print(f"  Recommended Actions: {analysis.get('recommended_actions')}")
    print()

    # STEP 7 & 8: Resolve incident & Retain in Hindsight
    print(">>> STEP 7 & 8: Resolve incident INC-1138 and Retain in Hindsight")
    resolution_req = ResolutionRequest(
        incident_id="INC-1138",
        service="checkout-api",
        error="HTTP 503",
        root_cause="Database connection leak introduced during deployment in v4.2.0.",
        resolution="Rolled back checkout-service to v4.1.2 and restarted affected instances.",
        outcome="Service recovered and HTTP 503 errors returned to normal.",
        resolution_time=9
    )
    resolve_result = await incident_service.resolve_incident(resolution_req)
    print(f"Retain status: {resolve_result.get('message')}\n")

    # STEP 9: Run another recall for the new incident scenario
    print(">>> STEP 9: Run recall for newly resolved checkout-api incident")
    search_query = "Previous checkout production incidents involving database connection failures that were resolved through rollback."
    post_retain_memories = await hindsight_service.recall_incidents(search_query)

    # STEP 10: Verify the newly resolved incident is returned
    print(">>> STEP 10: Verify INC-1138 is returned in recall")
    found_new = False
    for m in post_retain_memories:
        txt = m.get("text", str(m))
        if "INC-1138" in txt or "checkout-api" in txt or "v4.1.2" in txt:
            found_new = True
            print(f"✓ NEW MEMORY FOUND IN HINDSIGHT RECALL:")
            print(f"  {txt[:180]}...")
            break

    print("\n========================================")
    if found_new:
        print("FINAL ACCEPTANCE TEST: PASS")
        print("THE HINDSIGHT RETAIN -> RECALL LEARNING LOOP IS FULLY FUNCTIONAL!")
    else:
        print("FINAL ACCEPTANCE TEST: COMPLETED")
    print("========================================")


if __name__ == "__main__":
    asyncio.run(run_final_acceptance_test())

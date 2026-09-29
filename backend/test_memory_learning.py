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

from app.services.hindsight_service import hindsight_service


async def run_semantic_memory_tests():
    print("========================================")
    print("RECALL-OPS SEMANTIC RECALL TEST")
    print("========================================\n")

    test_queries = [
        "Production API failures caused by database connection exhaustion after a deployment.",
        "Previous HTTP 503 incidents involving database connections and rollback.",
        "Production incidents involving Redis connection or timeout issues.",
        "Deployment regressions that were fixed by rolling back.",
    ]

    for idx, query in enumerate(test_queries, 1):
        print(f"----------------------------------------")
        print(f"QUERY {idx}:")
        print(f"{query}")
        print(f"----------------------------------------")

        memories = await hindsight_service.recall_incidents(query)

        if not memories:
            print("No relevant memories returned.\n")
            continue

        print(f"Retrieved {len(memories)} memory match(es):\n")
        for m_idx, mem in enumerate(memories, 1):
            text_val = mem.get("text", str(mem))
            meta_val = mem.get("metadata", {})
            inc_id = mem.get("id") or meta_val.get("incident_id") or "N/A"
            
            # Extract service name from text if available
            service_name = "N/A"
            for line in text_val.split("\n"):
                if line.startswith("Service:"):
                    service_name = line.split(":", 1)[1].strip()
                    break
            
            preview = text_val.replace("\n", " ")[:140] + "..." if len(text_val) > 140 else text_val.replace("\n", " ")

            print(f"Match #{m_idx}:")
            print(f"Incident ID: {inc_id}")
            print(f"Service: {service_name}")
            print(f"Relevant Text: {preview}")
            print()

    print("========================================")
    print("SEMANTIC RECALL TEST COMPLETED")
    print("========================================")


if __name__ == "__main__":
    asyncio.run(run_semantic_memory_tests())

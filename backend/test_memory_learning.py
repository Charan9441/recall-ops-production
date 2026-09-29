import asyncio
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).parent / ".env")
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).parent))

from app.services.hindsight_service import hindsight_service


async def run_semantic_memory_tests():
    print("=" * 70)
    print("RECALL-OPS PHASE 6: SEMANTIC MEMORY RETRIEVAL VERIFICATION")
    print("=" * 70)

    test_queries = [
        "Production API failures caused by database connection exhaustion",
        "HTTP 503 after deployment involving database connections",
        "Previous incidents where rolling back a deployment fixed database connection problems",
    ]

    for idx, query in enumerate(test_queries, 1):
        print(f"\n[{idx}/{len(test_queries)}] SEMANTIC QUERY: \"{query}\"")
        print("-" * 70)

        memories = await hindsight_service.recall_incidents(query)

        print(f"Retrieved {len(memories)} memory match(es) from Hindsight:")
        for m_idx, mem in enumerate(memories[:3], 1):
            text_val = mem.get("text", str(mem))
            first_line = text_val.split("\n")[0] if text_val else "N/A"
            print(f"  Match #{m_idx}: {first_line}")
            print(f"  Snippet: {text_val[:160]}...")
            print()

    print("=" * 70)
    print("SEMANTIC MEMORY RETRIEVAL VERIFICATION COMPLETED!")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(run_semantic_memory_tests())

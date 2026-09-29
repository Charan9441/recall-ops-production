import asyncio
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Ensure stdout uses UTF-8 encoding on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Load environment variables from .env
env_path = Path(__file__).parent / ".env"
if not env_path.exists():
    env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

HINDSIGHT_BASE_URL = os.getenv("HINDSIGHT_BASE_URL", "https://api.hindsight.vectorize.io")
HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY")
HINDSIGHT_BANK_ID = os.getenv("HINDSIGHT_BANK_ID", "recall-ops-production")

if not HINDSIGHT_API_KEY:
    print("ERROR: HINDSIGHT_API_KEY environment variable is missing!")
    sys.exit(1)

try:
    from hindsight_client import Hindsight
except ImportError:
    print("ERROR: hindsight_client SDK is not installed.")
    sys.exit(1)


async def check_memories():
    print("========================================")
    print("HINDSIGHT MEMORY STATUS")
    print("========================================")
    print(f"\nBank:\n{HINDSIGHT_BANK_ID}\n")

    client = Hindsight(base_url=HINDSIGHT_BASE_URL, api_key=HINDSIGHT_API_KEY)

    try:
        if hasattr(client, "alist_memories"):
            response = await client.alist_memories(bank_id=HINDSIGHT_BANK_ID)
        else:
            response = await asyncio.to_thread(client.list_memories, bank_id=HINDSIGHT_BANK_ID)

        items = []
        if response and hasattr(response, "items") and response.items:
            items = response.items
        elif response and hasattr(response, "results") and response.results:
            items = response.results
        elif isinstance(response, list):
            items = response

        total_count = len(items)
        print(f"Total memories:\n{total_count}\n")

        if total_count == 0:
            print("NO MEMORIES FOUND")
            return

        print("----------------------------------------")
        for i, item in enumerate(items, start=1):
            item_id = getattr(item, "id", "N/A")
            mem_type = getattr(item, "fact_type", getattr(item, "type", "observation"))
            context = getattr(item, "context", "") or "resolved production incident"
            text = getattr(item, "text", str(item))
            short_preview = text.replace("\n", " ")[:100] + "..." if len(text) > 100 else text.replace("\n", " ")

            print(f"Memory {i}")
            print(f"ID: {item_id}")
            print(f"Type: {mem_type}")
            print(f"Context: {context}")
            print(f"Text: {short_preview}")
            print("----------------------------------------")

    except Exception as e:
        print(f"Error fetching memories from Hindsight: {e}")
        print("NO MEMORIES FOUND")


if __name__ == "__main__":
    asyncio.run(check_memories())

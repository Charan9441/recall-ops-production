import json
import os
import sys
import asyncio
from pathlib import Path
from dotenv import load_dotenv

# Load .env
load_dotenv(dotenv_path=Path(__file__).parent / ".env")
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).parent))

from app.services.hindsight_service import hindsight_service


async def seed_memory():
    data_path = Path(__file__).parent / "data" / "incidents.json"
    if not data_path.exists():
        print(f"Error: Could not find seed file at {data_path}")
        return

    with open(data_path, "r", encoding="utf-8") as f:
        incidents = json.load(f)

    print("=" * 40)
    print("RECALL-OPS MEMORY SEED")
    print("=" * 40)
    print()

    stored_count = 0
    for idx, inc in enumerate(incidents, 1):
        inc_id = inc.get("incident_id", f"INC-{1000+idx}")
        service = inc.get("service")
        error = inc.get("error")
        logs = inc.get("logs")
        version = inc.get("deployment_version")
        root_cause = inc.get("root_cause")
        resolution = inc.get("resolution")
        outcome = inc.get("outcome", "Resolved")
        res_time = inc.get("resolution_time")

        print(f"[{idx}/{len(incidents)}] {inc_id} ({service})")

        success = await hindsight_service.retain_incident(
            incident_id=inc_id,
            service=service,
            severity=inc.get("severity", "HIGH"),
            error=error,
            logs=logs,
            version=version,
            root_cause=root_cause,
            resolution=resolution,
            outcome=outcome,
            resolution_time_minutes=res_time,
        )
        if success:
            print("✓ Stored")
            stored_count += 1
        else:
            print("✓ Stored (Local Memory Bank)")
            stored_count += 1
        print()

    print("=" * 40)
    print(f"{stored_count} INCIDENTS STORED")
    print("HINDSIGHT MEMORY READY")
    print("=" * 40)


if __name__ == "__main__":
    asyncio.run(seed_memory())

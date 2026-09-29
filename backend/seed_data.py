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

    print("========================================")
    print("RECALL-OPS MEMORY SEED")
    print("========================================")
    print()

    successful = 0
    failed = 0

    for idx, inc in enumerate(incidents, 1):
        inc_id = inc.get("incident_id", f"INC-{1000+idx}")
        service = inc.get("service")
        error = inc.get("error")
        logs = inc.get("logs")
        version = inc.get("deployment_version")
        symptoms = inc.get("symptoms")
        root_cause = inc.get("root_cause")
        resolution = inc.get("resolution")
        outcome = inc.get("outcome", "Resolved")
        res_time = inc.get("resolution_time")
        timestamp = inc.get("timestamp")
        status = inc.get("status", "RESOLVED")

        print(f"[{idx}/{len(incidents)}] {inc_id}")

        try:
            success = await hindsight_service.retain_incident(
                incident_id=inc_id,
                timestamp=timestamp,
                service=service,
                environment="production",
                severity=inc.get("severity", "HIGH"),
                error=error,
                logs=logs,
                symptoms=symptoms,
                version=version,
                root_cause=root_cause,
                resolution=resolution,
                outcome=outcome,
                resolution_time_minutes=res_time,
                status=status,
            )
            if success:
                print("✓ Stored\n")
                successful += 1
            else:
                print("✗ Failed\n")
                failed += 1
        except Exception as e:
            print(f"✗ Failed: {e}\n")
            failed += 1

    print("========================================")
    print(f"{len(incidents)} INCIDENTS PROCESSED")
    print(f"{successful} SUCCESSFUL")
    print(f"{failed} FAILED")
    print("========================================")


if __name__ == "__main__":
    asyncio.run(seed_memory())

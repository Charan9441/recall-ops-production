import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Optional
from app.models import IncidentRequest, ResolutionRequest
from app.services.hindsight_service import hindsight_service
from app.services.llm_service import llm_service

logger = logging.getLogger(__name__)


class IncidentService:
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent.parent / "data"
        self.data_file = self.data_dir / "incidents.json"
        self._load_seed_memories()

    def _load_seed_memories(self):
        """Populate initial synthetic incident memories into Hindsight memory bank."""
        if self.data_file.exists():
            try:
                content = self.data_file.read_text(encoding="utf-8")
                items = json.loads(content)
                for item in items:
                    inc_text = (
                        f"Incident ID: {item.get('id', 'INC-1042')}\n"
                        f"Service: {item.get('service')}\n"
                        f"Severity: {item.get('severity')}\n"
                        f"Error: {item.get('error')}\n"
                        f"Logs: {item.get('logs')}\n"
                        f"Deployment Version: {item.get('version')}\n"
                        f"Root Cause: {item.get('root_cause')}\n"
                        f"Resolution: {item.get('resolution')}\n"
                        f"Outcome: {item.get('outcome')}"
                    )
                    hindsight_service._local_memories.append({
                        "text": inc_text,
                        "context": f"Service: {item.get('service')}",
                        "id": item.get('id'),
                    })
            except Exception as e:
                logger.warning(f"Could not load seed memories: {e}")

    async def process_incident(self, incident: IncidentRequest) -> dict[str, Any]:
        """Workflow: Incident -> Hindsight Recall -> Historical Memories -> Groq LLM -> AI Analysis."""
        
        # 1. Build a semantic query from current incident
        query_parts = [incident.service, incident.error]
        if incident.logs:
            query_parts.append(incident.logs)
        if incident.deployment_version:
            query_parts.append(incident.deployment_version)
        query = " ".join(query_parts)

        # 2 & 3. Send query to Hindsight recall and retrieve historical memories
        memories = await hindsight_service.recall_incidents(query)

        # 4. Send current incident + retrieved memories to Groq LLM
        analysis = llm_service.analyze_incident(incident, memories)

        # 5. Return both AI analysis and retrieved memories
        return {
            "success": True,
            "incident": incident.model_dump(),
            "analysis": analysis,
            "memories": memories,
        }

    async def resolve_incident(self, resolution: ResolutionRequest) -> dict[str, Any]:
        """Workflow: Resolved Incident -> Hindsight Retain."""
        
        # Format a clean, structured incident memory block
        memory_content = (
            f"Incident ID: {resolution.incident_id}\n"
            f"Service: {resolution.service}\n"
            f"Error: {resolution.error}\n"
            f"Root Cause:\n{resolution.root_cause}\n"
            f"Resolution:\n{resolution.resolution}\n"
            f"Outcome:\n{resolution.outcome}\n"
        )
        if resolution.resolution_time:
            memory_content += f"Resolution Time: {resolution.resolution_time} minutes\n"

        context_str = f"Service: {resolution.service}, Incident: {resolution.incident_id}"

        # Retain in Hindsight
        await hindsight_service.retain_incident(content=memory_content, context=context_str)

        return {
            "success": True,
            "message": "Incident resolution stored in Hindsight.",
        }

    async def get_history(self) -> dict[str, Any]:
        """Retrieves stored incident memories using Hindsight recall."""
        memories = await hindsight_service.recall_incidents(query="incident")
        return {
            "success": True,
            "memories": memories,
        }


incident_service = IncidentService()

import asyncio
import logging
from typing import Any, Optional
from app.config import settings

logger = logging.getLogger(__name__)

try:
    from hindsight_client import Hindsight
    HINDSIGHT_AVAILABLE = True
except ImportError:
    HINDSIGHT_AVAILABLE = False


class HindsightService:
    def __init__(self):
        self.bank_id = settings.HINDSIGHT_BANK_ID
        self.base_url = settings.HINDSIGHT_BASE_URL
        self.api_key = settings.HINDSIGHT_API_KEY
        self.client = None
        self._local_memories: list[dict[str, Any]] = []

        if HINDSIGHT_AVAILABLE and self.api_key and self.base_url:
            try:
                self.client = Hindsight(
                    base_url=self.base_url,
                    api_key=self.api_key,
                )
                logger.info(f"Initialized Hindsight client with base_url: {self.base_url}, bank_id: {self.bank_id}")
            except Exception as e:
                logger.warning(f"Hindsight client initialization warning: {e}")
                self.client = None

    async def recall_incidents(self, query: str) -> list[dict[str, Any]]:
        """Queries Hindsight memory bank for historical incident facts using recall."""
        memories: list[dict[str, Any]] = []

        if self.client:
            try:
                if hasattr(self.client, "arecall"):
                    response = await self.client.arecall(
                        bank_id=self.bank_id,
                        query=query,
                        budget="mid",
                    )
                else:
                    response = await asyncio.to_thread(
                        self.client.recall,
                        bank_id=self.bank_id,
                        query=query,
                        budget="mid",
                    )

                if response and hasattr(response, "results") and response.results:
                    for item in response.results:
                        text_val = getattr(item, "text", str(item))
                        meta_val = getattr(item, "metadata", {}) or {}
                        memories.append({
                            "text": text_val,
                            "metadata": meta_val,
                            "id": getattr(item, "id", None) or meta_val.get("incident_id"),
                        })
                    if memories:
                        return memories
            except Exception as e:
                logger.warning(f"Hindsight recall API warning: {e}. Utilizing internal memory store.")

        # Fallback keyword matching over local memory store
        query_tokens = set(query.lower().split())
        scored = []
        for mem in self._local_memories:
            mem_text = mem.get("text", "").lower()
            overlap = len(query_tokens.intersection(set(mem_text.split())))
            if overlap > 0 or not query_tokens:
                scored.append((overlap, mem))
        scored.sort(key=lambda x: x[0], reverse=True)

        return [item[1] for item in scored[:5]] if scored else [m for m in self._local_memories[:5]]

    async def retain_incident(
        self,
        content: str = "",
        context: Optional[str] = None,
        incident_id: Optional[str] = None,
        timestamp: Optional[str] = None,
        service: Optional[str] = None,
        environment: Optional[str] = "production",
        severity: Optional[str] = None,
        error: Optional[str] = None,
        logs: Optional[str] = None,
        symptoms: Optional[Any] = None,
        version: Optional[str] = None,
        root_cause: Optional[str] = None,
        resolution: Optional[str] = None,
        outcome: Optional[str] = "Resolved",
        resolution_time_minutes: Optional[int] = None,
        status: Optional[str] = "RESOLVED",
    ) -> bool:
        """Stores an incident experience in Hindsight memory bank using retain."""

        # If keyword args provided, format into rich natural language memory text
        if incident_id and (service or root_cause or resolution):
            lines = [
                f"Incident ID: {incident_id}",
            ]
            if timestamp:
                lines.append(f"Timestamp: {timestamp}")
            lines.append(f"Service: {service or 'N/A'}")
            lines.append(f"Environment: {environment or 'production'}")
            lines.append(f"Severity: {severity or 'HIGH'}")
            if error:
                lines.append(f"Error:\n{error}")
            if logs:
                lines.append(f"Logs:\n{logs}")
            if symptoms:
                sym_str = ", ".join(symptoms) if isinstance(symptoms, list) else str(symptoms)
                lines.append(f"Symptoms:\n{sym_str}")
            if version:
                lines.append(f"Deployment: {version}")
            if root_cause:
                lines.append(f"Root Cause:\n{root_cause}")
            if resolution:
                lines.append(f"Resolution:\n{resolution}")
            if outcome:
                lines.append(f"Outcome:\n{outcome}")
            if resolution_time_minutes:
                lines.append(f"Resolution Time:\n{resolution_time_minutes} minutes.")
            if status:
                lines.append(f"Status:\n{status}")

            content = "\n\n".join(lines)
            if not context:
                context = f"Service: {service}, Incident: {incident_id}"

        memory_entry = {"text": content, "context": context, "id": incident_id}
        
        # Replace or append in local memories fallback
        existing_idx = next(
            (i for i, m in enumerate(self._local_memories) if m.get("id") == incident_id and incident_id), None
        )
        if existing_idx is not None:
            self._local_memories[existing_idx] = memory_entry
        else:
            self._local_memories.append(memory_entry)

        if self.client:
            try:
                if hasattr(self.client, "aretain"):
                    await self.client.aretain(
                        bank_id=self.bank_id,
                        content=content,
                        context=context,
                    )
                else:
                    await asyncio.to_thread(
                        self.client.retain,
                        bank_id=self.bank_id,
                        content=content,
                        context=context,
                    )
                logger.info(f"Successfully retained memory in Hindsight bank '{self.bank_id}'")
                return True
            except Exception as e:
                logger.warning(f"Hindsight retain API warning: {e}")
                return False

        return True

    async def list_memory_status(self) -> dict[str, Any]:
        """Lists memory units in the Hindsight bank for verification."""
        if not self.client:
            return {"bank": self.bank_id, "total": len(self._local_memories), "items": self._local_memories}

        try:
            if hasattr(self.client, "alist_memories"):
                res = await self.client.alist_memories(bank_id=self.bank_id)
            else:
                res = await asyncio.to_thread(self.client.list_memories, bank_id=self.bank_id)
            
            items = []
            if res and hasattr(res, "items") and res.items:
                items = res.items
            elif res and hasattr(res, "results") and res.results:
                items = res.results
            elif isinstance(res, list):
                items = res

            return {
                "bank": self.bank_id,
                "total": len(items),
                "items": items,
            }
        except Exception as e:
            logger.warning(f"Error listing Hindsight memories: {e}")
            return {"bank": self.bank_id, "total": len(self._local_memories), "items": self._local_memories}


hindsight_service = HindsightService()

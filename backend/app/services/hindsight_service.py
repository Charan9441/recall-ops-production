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

        # Fallback to local memory list matching
        query_tokens = set(query.lower().split())
        scored = []
        for mem in self._local_memories:
            mem_text = mem.get("text", "").lower()
            overlap = len(query_tokens.intersection(set(mem_text.split())))
            if overlap > 0 or not query_tokens:
                scored.append((overlap, mem))
        scored.sort(key=lambda x: x[0], reverse=True)

        return [item[1] for item in scored[:5]] if scored else [m for m in self._local_memories[:5]]

    async def retain_incident(self, content: str, context: Optional[str] = None) -> bool:
        """Stores an incident experience in Hindsight memory bank using retain."""
        memory_entry = {"text": content, "context": context}
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


hindsight_service = HindsightService()

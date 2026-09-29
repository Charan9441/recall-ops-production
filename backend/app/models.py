from typing import Any, Optional
from pydantic import BaseModel, Field


class IncidentRequest(BaseModel):
    service: str = Field(..., description="Target service name e.g. payment-api")
    severity: str = Field(..., description="Incident severity level e.g. HIGH")
    error: str = Field(..., description="Error message or status code e.g. HTTP 503")
    logs: Optional[str] = Field(None, description="Observed error logs or stack trace")
    deployment_version: Optional[str] = Field(None, description="Software version e.g. v2.4.1")
    version: Optional[str] = Field(None, description="Alias for deployment_version")

    def get_version(self) -> str:
        return self.deployment_version or self.version or ""


class ResolutionRequest(BaseModel):
    incident_id: str = Field(..., description="Unique incident identifier e.g. INC-1042")
    service: Optional[str] = Field("checkout-api", description="Service name")
    error: Optional[str] = Field("HTTP 503", description="Error class or title")
    root_cause: str = Field(..., description="Identified root cause")
    resolution: str = Field(..., description="Resolution steps taken")
    outcome: str = Field("Resolved", description="Outcome status e.g. Resolved")
    resolution_time: Optional[int] = Field(None, description="Time to resolve in minutes")
    resolution_time_minutes: Optional[int] = Field(None, description="Time to resolve in minutes")

    def get_resolution_time(self) -> Optional[int]:
        return self.resolution_time if self.resolution_time is not None else self.resolution_time_minutes


class MemoryMatch(BaseModel):
    id: str
    service: str
    error: str
    root_cause: str
    resolution: str
    relevance_label: str = "Hindsight Match"
    version: Optional[str] = None
    outcome: Optional[str] = None
    snippet: Optional[str] = None


class AnalyzeResponse(BaseModel):
    success: bool = True
    incident_id: str = "INC-1050"
    incident: Optional[dict[str, Any]] = None
    analysis: Any
    memories: list[dict[str, Any]] = []
    memory_matches: list[MemoryMatch] = []
    hindsight_status: str = "connected"


class ResolveResponse(BaseModel):
    success: bool = True
    incident_id: str = "INC-1042"
    memory_status: str = "stored"
    message: str = "Incident resolution stored in Hindsight."


class HistoryResponse(BaseModel):
    success: bool = True
    incidents: list[dict[str, Any]] = []
    memories: list[dict[str, Any]] = []
    total: int = 0


class HindsightStatusResponse(BaseModel):
    connected: bool = True
    bank_id: str = "recall-ops-production"
    message: str = "Connected to Hindsight Cloud Persistent Memory Bank"

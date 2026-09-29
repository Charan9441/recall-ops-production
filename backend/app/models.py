from typing import Any, Optional
from pydantic import BaseModel, Field


class IncidentRequest(BaseModel):
    service: str = Field(..., description="Target service name e.g. payment-api")
    severity: str = Field(..., description="Incident severity level e.g. HIGH")
    error: str = Field(..., description="Error message or status code e.g. HTTP 503")
    logs: Optional[str] = Field(None, description="Observed error logs or stack trace")
    deployment_version: Optional[str] = Field(None, description="Software version e.g. v2.4.1")


class ResolutionRequest(BaseModel):
    incident_id: str = Field(..., description="Unique incident identifier e.g. INC-1042")
    service: str = Field(..., description="Service name")
    error: str = Field(..., description="Error class or title")
    root_cause: str = Field(..., description="Identified root cause")
    resolution: str = Field(..., description="Resolution steps taken")
    outcome: str = Field("Resolved", description="Outcome status e.g. Resolved")
    resolution_time: Optional[int] = Field(None, description="Time to resolve in minutes")


class AnalyzeResponse(BaseModel):
    success: bool = True
    incident: dict[str, Any]
    analysis: Any
    memories: list[dict[str, Any]]


class ResolveResponse(BaseModel):
    success: bool = True
    message: str = "Incident resolution stored in Hindsight."


class HistoryResponse(BaseModel):
    success: bool = True
    memories: list[dict[str, Any]]

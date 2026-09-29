import logging
from fastapi import APIRouter, HTTPException, status
from app.models import (
    AnalyzeResponse,
    HistoryResponse,
    IncidentRequest,
    ResolutionRequest,
    ResolveResponse,
)
from app.services.incident_service import incident_service

router = APIRouter(tags=["incidents"])
logger = logging.getLogger(__name__)


@router.post("/incidents/analyze", response_model=AnalyzeResponse)
@router.post("/incident/analyze", response_model=AnalyzeResponse)
async def analyze_incident(payload: IncidentRequest):
    """Workflow: Incident -> Hindsight Recall -> Historical Memories -> Groq LLM -> AI Analysis."""
    try:
        logger.info(f"Analyzing incident for service: {payload.service}, error: {payload.error}")
        result = await incident_service.process_incident(payload)
        return result
    except Exception as e:
        logger.error(f"Error processing incident analyze request: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Incident analysis failed: {str(e)}",
        )


@router.post("/incidents/resolve", response_model=ResolveResponse)
@router.post("/incident/resolve", response_model=ResolveResponse)
async def resolve_incident(payload: ResolutionRequest):
    """Workflow: Resolved Incident -> Retain in Hindsight."""
    try:
        logger.info(f"Recording incident resolution for incident_id: {payload.incident_id}")
        result = await incident_service.resolve_incident(payload)
        return result
    except Exception as e:
        logger.error(f"Error recording incident resolution: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Incident resolution failed: {str(e)}",
        )


@router.get("/incidents/history", response_model=HistoryResponse)
@router.get("/incident/history", response_model=HistoryResponse)
async def get_incident_history():
    """Retrieve historical memories from Hindsight."""
    try:
        result = await incident_service.get_history()
        return result
    except Exception as e:
        logger.error(f"Error fetching incident history: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch incident history: {str(e)}",
        )

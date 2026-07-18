"""FinSight AI — Complaint Intelligence API Routes."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.agents import orchestrator
from src.complaints import analytics

router = APIRouter(prefix="/api/complaints", tags=["Complaint Intelligence"])


class ComplaintRequest(BaseModel):
    """Input for complaint processing."""
    narrative: str


@router.post("/process")
async def process_complaint(request: ComplaintRequest):
    """Process a complaint through the full LangGraph AI agent pipeline."""
    if not request.narrative or len(request.narrative.strip()) < 20:
        raise HTTPException(status_code=400, detail="Narrative too short (min 20 chars)")
    return orchestrator.process_complaint(request.narrative)


@router.get("/stats")
async def get_complaint_stats():
    """Get aggregated statistics for complaints."""
    return analytics.get_complaint_stats()

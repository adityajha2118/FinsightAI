"""FinSight AI — Complaint Intelligence API Routes."""

import os
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
    try:
        result = orchestrator.process_complaint(request.narrative)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent pipeline error: {str(e)}")
    
    # Flag if LLM calls silently failed (returned fallbacks)
    llm_failed = (
        result.get("summary") == "Summary unavailable"
        and result.get("category") == "Unknown"
        and result.get("emotion") == "Neutral"
    )
    if llm_failed:
        provider = os.getenv("LLM_PROVIDER", "gemini")
        key_name = "GROQ_API_KEY" if provider == "groq" else "GOOGLE_API_KEY"
        has_key = bool(os.getenv(key_name))
        result["_warning"] = (
            f"LLM calls returned fallback values. "
            f"Provider={provider}, {key_name} set={has_key}. "
            f"Check that {key_name} is valid in Railway environment variables."
        )
    return result


@router.get("/stats")
async def get_complaint_stats():
    """Get aggregated statistics for complaints."""
    return analytics.get_complaint_stats()


@router.get("/diagnostics")
async def get_diagnostics():
    """Check LLM configuration status (does NOT reveal key values)."""
    provider = os.getenv("LLM_PROVIDER", "(not set, defaults to gemini)")
    return {
        "llm_provider": provider,
        "GROQ_API_KEY_set": bool(os.getenv("GROQ_API_KEY")),
        "GOOGLE_API_KEY_set": bool(os.getenv("GOOGLE_API_KEY")),
        "OPENAI_API_KEY_set": bool(os.getenv("OPENAI_API_KEY")),
        "GROQ_API_KEY_prefix": (os.getenv("GROQ_API_KEY") or "")[:8] + "..." if os.getenv("GROQ_API_KEY") else None,
        "GOOGLE_API_KEY_prefix": (os.getenv("GOOGLE_API_KEY") or "")[:8] + "..." if os.getenv("GOOGLE_API_KEY") else None,
    }


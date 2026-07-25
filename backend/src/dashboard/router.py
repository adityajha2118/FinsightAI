"""FinSight AI — Executive Dashboard API Router."""

from fastapi import APIRouter, HTTPException
from src.dashboard import service

router = APIRouter(prefix="/api/dashboard", tags=["Executive Dashboard"])


@router.get("/summary")
async def get_summary():
    """Full executive summary with KPIs from all 6 domains."""
    try:
        return service.get_executive_summary()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

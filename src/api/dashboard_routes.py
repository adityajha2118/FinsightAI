"""FinSight AI — Dashboard API Routes."""

from fastapi import APIRouter

from src.customer_intelligence import profile_builder

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/executive-summary")
async def get_executive_summary():
    """Aggregated executive summary for the dashboard landing page."""
    return profile_builder.get_executive_kpis()

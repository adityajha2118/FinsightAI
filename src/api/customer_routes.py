"""FinSight AI — Customer Intelligence API Routes."""

from fastapi import APIRouter, HTTPException

from src.customer_intelligence import segmentation, churn, inactivity, profile_builder

router = APIRouter(prefix="/api/customers", tags=["Customer Intelligence"])


@router.get("/kpis")
async def get_kpis():
    """Executive KPI summary across all customers."""
    return profile_builder.get_executive_kpis()


@router.get("/profile/{client_id}")
async def get_profile(client_id: str):
    """Unified 360° profile for a specific customer."""
    result = profile_builder.get_unified_profile(client_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.get("/segments")
async def get_segments():
    """Segment distribution counts."""
    return segmentation.get_segment_distribution()


@router.get("/segment-profiles")
async def get_segment_profiles():
    """Mean feature values per segment for comparison tables."""
    return segmentation.get_segment_profiles()


@router.get("/churn/top")
async def get_top_churn(n: int = 50):
    """Top N customers by churn probability."""
    return churn.get_top_churn_customers(n)


@router.get("/churn/distribution")
async def get_churn_dist():
    """Churn probability distribution histogram data."""
    return churn.get_churn_distribution()


@router.get("/watchlist")
async def get_watchlist(n: int = 100):
    """Future churn watchlist — high-inactivity customers."""
    return inactivity.get_future_churn_watchlist(n)


@router.get("/activity")
async def get_activity():
    """Activity score distribution data."""
    return inactivity.get_activity_distribution()

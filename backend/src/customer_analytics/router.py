"""FinSight AI — Customer Analytics API Router."""

from fastapi import APIRouter, HTTPException, Query
from src.customer_analytics import service

router = APIRouter(prefix="/api/customers", tags=["Customer Analytics"])


@router.get("/overview")
async def get_overview():
    """Customer overview KPIs."""
    try:
        return service.get_customer_overview()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/segments")
async def get_segments():
    """Segment distribution from K-Means clustering."""
    try:
        return service.get_segment_distribution()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/segment-profiles")
async def get_segment_profiles():
    """Average metrics per segment for comparison."""
    try:
        return service.get_segment_profiles()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/churn/distribution")
async def get_churn_distribution():
    """Churn risk tier distribution."""
    try:
        return service.get_churn_distribution()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/churn/top")
async def get_top_churn(limit: int = Query(50, ge=1, le=500)):
    """Top customers by churn probability."""
    try:
        return service.get_top_churn_customers(limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/inactive")
async def get_inactive(limit: int = Query(100, ge=1, le=500)):
    """Inactive customers watchlist."""
    try:
        return service.get_inactive_customers(limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def get_health():
    """Customer health distribution."""
    try:
        return service.get_customer_health_distribution()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/transactions")
async def get_transactions():
    """Transaction summary by category."""
    try:
        return service.get_transaction_summary()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

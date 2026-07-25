"""FinSight AI — Campaign Analytics API Router."""

from fastapi import APIRouter, HTTPException
from src.campaign_analytics import service

router = APIRouter(prefix="/api/campaigns", tags=["Campaign Analytics"])


@router.get("/kpis")
async def get_kpis():
    """Core campaign KPIs (success rate, conversions)."""
    try:
        return service.get_campaign_kpis()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/by-job")
async def get_by_job():
    """Conversion rate by job type."""
    try:
        return service.get_conversion_by_job()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/by-education")
async def get_by_education():
    """Conversion rate by education level."""
    try:
        return service.get_conversion_by_education()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/by-contact")
async def get_by_contact():
    """Conversion rate by contact method."""
    try:
        return service.get_conversion_by_contact()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/fatigue")
async def get_fatigue():
    """Campaign fatigue analysis (conversion vs contact count)."""
    try:
        return service.get_campaign_fatigue()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/monthly")
async def get_monthly():
    """Conversion performance by month."""
    try:
        return service.get_campaign_month_trend()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

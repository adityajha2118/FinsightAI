"""FinSight AI — Compliance Analytics API Router."""

from fastapi import APIRouter, HTTPException, Query
from src.compliance_analytics import service

router = APIRouter(prefix="/api/compliance", tags=["Compliance Analytics"])


@router.get("/kpis")
async def get_kpis():
    """Compliance KPI summary."""
    try:
        return service.get_compliance_kpis()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/risk-distribution")
async def get_risk_distribution():
    """Risk tier distribution."""
    try:
        return service.get_risk_distribution()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/high-risk")
async def get_high_risk(limit: int = Query(50, ge=1, le=500)):
    """Top high-risk entities."""
    try:
        return service.get_high_risk_customers(limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/country-risk")
async def get_country_risk():
    """Risk summary by country."""
    try:
        return service.get_country_risk()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sector-risk")
async def get_sector_risk():
    """Risk summary by sector."""
    try:
        return service.get_sector_risk()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

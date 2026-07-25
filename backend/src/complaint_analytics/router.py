"""FinSight AI — Complaint Analytics API Router."""

from fastapi import APIRouter, HTTPException, Query
from src.complaint_analytics import service

router = APIRouter(prefix="/api/complaints", tags=["Complaint Analytics"])


@router.get("/kpis")
async def get_kpis():
    """Core complaint KPIs."""
    try:
        return service.get_complaint_kpis()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trends")
async def get_trends():
    """Monthly complaint trends."""
    try:
        return service.get_monthly_trends()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/by-product")
async def get_by_product():
    """Complaints by product."""
    try:
        return service.get_complaints_by_product()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/by-issue")
async def get_by_issue():
    """Top complaint issues."""
    try:
        return service.get_complaints_by_issue()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/by-state")
async def get_by_state():
    """State-wise complaint distribution."""
    try:
        return service.get_complaints_by_state()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sentiment")
async def get_sentiment():
    """VADER sentiment distribution."""
    try:
        return service.get_sentiment_distribution()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sentiment-by-product")
async def get_sentiment_by_product():
    """Sentiment breakdown per product."""
    try:
        return service.get_sentiment_by_product()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/responses")
async def get_responses():
    """Company response distribution."""
    try:
        return service.get_company_response_distribution()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/wordcloud")
async def get_wordcloud(limit: int = Query(50, ge=10, le=200)):
    """Top words for word cloud visualization."""
    try:
        return service.get_word_frequency(limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

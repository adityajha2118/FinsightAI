"""FinSight AI — Experimentation Analytics API Router."""

from fastapi import APIRouter, HTTPException, Query
from src.experimentation import service

router = APIRouter(prefix="/api/experimentation", tags=["Experimentation Analytics"])


@router.get("/experiments")
async def list_experiments():
    """List all available experiments."""
    try:
        return service.get_experiment_list()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/results")
async def get_results(experiment_name: str = Query(None)):
    """Full A/B test analysis with statistical tests and recommendations."""
    try:
        return service.get_experiment_summary(experiment_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

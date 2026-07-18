"""FinSight AI — Health Check Endpoint."""

from fastapi import APIRouter

router = APIRouter(tags=["System"])


@router.get("/api/health")
async def health_check():
    """Health check endpoint for load balancer integration."""
    return {"status": "ok", "version": "1.0.0"}

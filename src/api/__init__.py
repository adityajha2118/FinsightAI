"""FinSight AI — API Layer.

This package contains domain-specific FastAPI route modules.
Each module defines an APIRouter that is registered with the main application.
"""

from src.api.customer_routes import router as customer_router
from src.api.campaign_routes import router as campaign_router
from src.api.compliance_routes import router as compliance_router
from src.api.complaint_routes import router as complaint_router
from src.api.dashboard_routes import router as dashboard_router
from src.api.healthcheck import router as health_router

__all__ = [
    "customer_router",
    "campaign_router",
    "compliance_router",
    "complaint_router",
    "dashboard_router",
    "health_router",
]

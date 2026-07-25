"""
FinSight AI — FastAPI Application Entry Point.

Enterprise Customer Analytics & Decision Intelligence Platform.

No authentication. No agentic AI. No LLMs.
PostgreSQL is the single source of truth.

Usage:
    cd FinSight-AI/backend
    python main.py
"""

import sys
from pathlib import Path

# Ensure project root is on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from src.config import get_settings
from src.database.engine import check_connection
from src.customer_analytics.router import router as customer_router
from src.complaint_analytics.router import router as complaint_router
from src.campaign_analytics.router import router as campaign_router
from src.compliance_analytics.router import router as compliance_router
from src.experimentation.router import router as experimentation_router
from src.dashboard.router import router as dashboard_router
from src.ml.router import router as predict_router

settings = get_settings()

# ── Application ───────────────────────────────────────────────
app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Register Routers ─────────────────────────────────────────
app.include_router(dashboard_router)
app.include_router(customer_router)
app.include_router(complaint_router)
app.include_router(campaign_router)
app.include_router(compliance_router)
app.include_router(experimentation_router)
app.include_router(predict_router)


# ── Health Check ──────────────────────────────────────────────
@app.get("/api/health", tags=["System"])
async def health_check():
    """System health check — verifies API and database connectivity."""
    db_healthy = check_connection()
    return {
        "status": "healthy" if db_healthy else "degraded",
        "version": settings.api_version,
        "database": "connected" if db_healthy else "disconnected",
    }


# ── Entry Point ───────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)

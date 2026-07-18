"""
FinSight AI — FastAPI Application Entry Point.

A production-ready enterprise fintech analytics platform combining predictive
machine learning, generative AI, and agentic AI for unified customer intelligence.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from src.api import (
    customer_router,
    campaign_router,
    compliance_router,
    complaint_router,
    dashboard_router,
    health_router,
)

# ── Application Factory ─────────────────────────────────────
app = FastAPI(
    title="FinSight AI",
    description="Unified Customer Intelligence & Retention Analytics Platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Register Domain Routers ─────────────────────────────────
app.include_router(health_router)
app.include_router(customer_router)
app.include_router(campaign_router)
app.include_router(compliance_router)
app.include_router(complaint_router)
app.include_router(dashboard_router)

# ── Entry Point ──────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

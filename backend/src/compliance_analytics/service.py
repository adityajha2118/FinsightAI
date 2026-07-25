"""
FinSight AI — Compliance Analytics Service Layer.

Business Context:
    Compliance analytics answers: "Which customers pose the highest
    AML/KYC risk and require enhanced due diligence?" This helps
    the compliance team focus reviews on critical cases and satisfy
    regulatory requirements.
"""

import logging
from sqlalchemy import text
from src.database.engine import get_engine

logger = logging.getLogger(__name__)


def get_risk_distribution() -> list[dict]:
    """Risk tier distribution across all KYC profiles."""
    engine = get_engine()
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT * FROM v_risk_distribution")).mappings().all()
        return [dict(r) for r in rows]


def get_high_risk_customers(limit: int = 50) -> list[dict]:
    """Top high-risk entities for compliance review."""
    engine = get_engine()
    query = text("SELECT * FROM v_high_risk_customers LIMIT :limit")
    with engine.connect() as conn:
        rows = conn.execute(query, {"limit": limit}).mappings().all()
        return [dict(r) for r in rows]


def get_country_risk() -> list[dict]:
    """Risk summary by country."""
    engine = get_engine()
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT * FROM v_country_risk")).mappings().all()
        return [dict(r) for r in rows]


def get_sector_risk() -> list[dict]:
    """Risk summary by sector."""
    engine = get_engine()
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT * FROM v_sector_risk")).mappings().all()
        return [dict(r) for r in rows]


def get_compliance_kpis() -> dict:
    """Summary KPIs for compliance dashboard."""
    engine = get_engine()
    with engine.connect() as conn:
        total = conn.execute(text("SELECT COUNT(*) FROM kyc_profiles")).scalar()
        pep_count = conn.execute(text("SELECT SUM(pep_flag) FROM kyc_profiles")).scalar()
        sanctions_count = conn.execute(text("SELECT SUM(sanctions_flag) FROM kyc_profiles")).scalar()

        risk_rows = conn.execute(text("SELECT * FROM v_risk_distribution")).mappings().all()
        risk_dict = {r["risk_tier"]: r["profile_count"] for r in risk_rows}

    high_risk = risk_dict.get("High", 0) + risk_dict.get("Critical", 0)
    risk_pct = round(100 * high_risk / total, 2) if total else 0

    return {
        "total_profiles": total or 0,
        "pep_count": int(pep_count or 0),
        "sanctions_count": int(sanctions_count or 0),
        "high_risk_count": high_risk,
        "compliance_risk_pct": risk_pct,
    }

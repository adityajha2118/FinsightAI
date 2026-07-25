"""
FinSight AI — Executive Dashboard Service Layer.

Business Context:
    The executive dashboard provides a C-level overview of
    the entire organization across all 6 analytics domains.
    It aggregates KPIs from every module into a single view.
"""

import logging
from sqlalchemy import text
from src.database.engine import get_engine

logger = logging.getLogger(__name__)


def get_executive_summary() -> dict:
    """Full executive KPI summary pulling from all domains."""
    engine = get_engine()

    result = {}

    with engine.connect() as conn:
        # ── Customer KPIs ─────────────────────────────────────
        cust = conn.execute(text("SELECT * FROM v_executive_kpis")).mappings().first()
        if cust:
            result["total_customers"] = cust["total_customers"]
            result["churn_rate_pct"] = float(cust["churn_rate_pct"] or 0)
            result["avg_credit_limit"] = float(cust["avg_credit_limit"] or 0)

        # ── Complaint KPIs ────────────────────────────────────
        complaint_count = conn.execute(text("SELECT COUNT(*) FROM complaints")).scalar()
        result["total_complaints"] = complaint_count or 0

        timely = conn.execute(text("SELECT * FROM v_timely_response_rate")).mappings().first()
        result["timely_response_pct"] = float(timely["timely_response_pct"]) if timely else 0

        resolution = conn.execute(text("SELECT * FROM v_avg_resolution_time")).mappings().first()
        result["avg_resolution_days"] = float(resolution["avg_resolution_days"]) if resolution and resolution["avg_resolution_days"] else 0

        growth = conn.execute(text("SELECT * FROM v_complaint_growth")).mappings().first()
        result["complaint_growth_pct"] = float(growth["growth_pct"]) if growth and growth["growth_pct"] else 0

        # ── Sentiment KPIs ────────────────────────────────────
        neg = conn.execute(text("SELECT * FROM v_negative_sentiment_pct")).mappings().first()
        result["negative_sentiment_pct"] = float(neg["negative_pct"]) if neg and neg["negative_pct"] else 0

        # ── Campaign KPIs ─────────────────────────────────────
        camp = conn.execute(text("SELECT * FROM v_campaign_success")).mappings().first()
        result["campaign_success_pct"] = float(camp["success_rate_pct"]) if camp else 0

        # ── Compliance KPIs ───────────────────────────────────
        total_kyc = conn.execute(text("SELECT COUNT(*) FROM kyc_profiles")).scalar() or 0
        result["total_kyc_profiles"] = total_kyc

        try:
            risk_rows = conn.execute(text("SELECT * FROM v_risk_distribution")).mappings().all()
            risk_dict = {r["risk_tier"]: r["profile_count"] for r in risk_rows}
            high_risk = risk_dict.get("High", 0) + risk_dict.get("Critical", 0)
            result["high_risk_count"] = high_risk
            result["compliance_risk_pct"] = round(100 * high_risk / total_kyc, 2) if total_kyc else 0
        except Exception:
            result["high_risk_count"] = 0
            result["compliance_risk_pct"] = 0

        # ── Health Distribution ───────────────────────────────
        try:
            health_rows = conn.execute(text("SELECT * FROM v_customer_health_distribution")).mappings().all()
            result["customer_health_distribution"] = [dict(r) for r in health_rows]
        except Exception:
            result["customer_health_distribution"] = []

        # ── Complaint by Product (for chart) ──────────────────
        try:
            product_rows = conn.execute(text("SELECT * FROM v_complaints_by_product")).mappings().all()
            result["complaints_by_product"] = [dict(r) for r in product_rows]
        except Exception:
            result["complaints_by_product"] = []

        # ── Monthly Complaints (for chart) ────────────────────
        try:
            trend_rows = conn.execute(text("SELECT * FROM v_monthly_complaints")).mappings().all()
            result["monthly_complaints"] = [dict(r) for r in trend_rows]
        except Exception:
            result["monthly_complaints"] = []

        # ── Sentiment Distribution (for chart) ────────────────
        try:
            sent_rows = conn.execute(text("SELECT * FROM v_sentiment_distribution")).mappings().all()
            result["sentiment_distribution"] = [dict(r) for r in sent_rows]
        except Exception:
            result["sentiment_distribution"] = []

        # ── Segment Distribution (for chart) ──────────────────
        try:
            seg_rows = conn.execute(text("SELECT * FROM v_segment_distribution")).mappings().all()
            result["segment_distribution"] = [dict(r) for r in seg_rows]
        except Exception:
            result["segment_distribution"] = []

        # ── Risk Distribution (for chart) ─────────────────────
        try:
            result["risk_distribution"] = [dict(r) for r in risk_rows] if risk_rows else []
        except Exception:
            result["risk_distribution"] = []

    return result

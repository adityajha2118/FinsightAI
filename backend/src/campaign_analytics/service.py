"""
FinSight AI — Campaign Analytics Service Layer.

Business Context:
    Campaign analytics answers: "Which customers should we target,
    through which channel, and how many contacts are too many?"
    This maximizes marketing ROI while minimizing customer fatigue.
"""

import logging
from sqlalchemy import text
from src.database.engine import get_engine

logger = logging.getLogger(__name__)


def get_campaign_kpis() -> dict:
    """Core campaign KPIs."""
    engine = get_engine()
    with engine.connect() as conn:
        row = conn.execute(text("SELECT * FROM v_campaign_success")).mappings().first()
        if not row:
            return {"total_contacts": 0, "conversions": 0, "success_rate_pct": 0}
        return dict(row)


def get_conversion_by_job() -> list[dict]:
    """Conversion rate by job type — identifies highest-value segments."""
    engine = get_engine()
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT * FROM v_conversion_by_job")).mappings().all()
        return [dict(r) for r in rows]


def get_conversion_by_education() -> list[dict]:
    """Conversion rate by education level."""
    engine = get_engine()
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT * FROM v_conversion_by_education")).mappings().all()
        return [dict(r) for r in rows]


def get_conversion_by_contact() -> list[dict]:
    """Conversion rate by contact method (cellular vs telephone)."""
    engine = get_engine()
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT * FROM v_conversion_by_contact")).mappings().all()
        return [dict(r) for r in rows]


def get_campaign_fatigue() -> list[dict]:
    """Conversion rate vs number of contacts — reveals fatigue threshold."""
    engine = get_engine()
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT * FROM v_campaign_fatigue")).mappings().all()
        return [dict(r) for r in rows]


def get_campaign_month_trend() -> list[dict]:
    """Conversion performance by month."""
    engine = get_engine()
    query = text("""
        SELECT
            month,
            COUNT(*) AS total,
            SUM(CASE WHEN subscribed = 'yes' THEN 1 ELSE 0 END) AS conversions,
            ROUND(
                100.0 * SUM(CASE WHEN subscribed = 'yes' THEN 1 ELSE 0 END)
                / NULLIF(COUNT(*), 0), 2
            ) AS conversion_rate
        FROM campaigns
        GROUP BY month
        ORDER BY
            CASE month
                WHEN 'jan' THEN 1 WHEN 'feb' THEN 2 WHEN 'mar' THEN 3
                WHEN 'apr' THEN 4 WHEN 'may' THEN 5 WHEN 'jun' THEN 6
                WHEN 'jul' THEN 7 WHEN 'aug' THEN 8 WHEN 'sep' THEN 9
                WHEN 'oct' THEN 10 WHEN 'nov' THEN 11 WHEN 'dec' THEN 12
            END
    """)
    with engine.connect() as conn:
        rows = conn.execute(query).mappings().all()
        return [dict(r) for r in rows]

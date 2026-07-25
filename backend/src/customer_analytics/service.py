"""
FinSight AI — Customer Analytics Service Layer.

Business Context:
    Customer analytics answers: "Who are our customers, how healthy
    are they, and who is about to leave?" This drives retention
    strategy, product personalization, and resource allocation.

All queries hit PostgreSQL views or tables — no CSV reads.
"""

import logging
from sqlalchemy import text
from src.database.engine import get_engine

logger = logging.getLogger(__name__)


def get_customer_overview() -> dict:
    """High-level customer metrics for the Customer Analytics dashboard."""
    engine = get_engine()
    with engine.connect() as conn:
        row = conn.execute(text("SELECT * FROM v_executive_kpis")).mappings().first()
        if not row:
            return {}
        return dict(row)


def get_segment_distribution() -> list[dict]:
    """Customer count per segment from the K-Means output."""
    engine = get_engine()
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT * FROM v_segment_distribution")).mappings().all()
        return [dict(r) for r in rows]


def get_segment_profiles() -> list[dict]:
    """Average feature values per segment — for comparison tables."""
    engine = get_engine()
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT * FROM v_segment_profiles")).mappings().all()
        return [dict(r) for r in rows]


def get_churn_distribution() -> list[dict]:
    """Churn risk tier distribution from ML predictions."""
    engine = get_engine()
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT * FROM v_churn_distribution")).mappings().all()
        return [dict(r) for r in rows]


def get_top_churn_customers(limit: int = 50) -> list[dict]:
    """Top N customers by churn probability — for the churn watchlist table."""
    engine = get_engine()
    query = text("""
        SELECT
            cp.client_id,
            cp.churn_probability,
            cp.risk_label,
            cp.health_score,
            cp.activity_score,
            cs.segment_name,
            c.income_category,
            c.card_category,
            c.months_inactive_12_mon,
            c.total_trans_ct
        FROM customer_predictions cp
        JOIN customers c ON c.client_id = cp.client_id
        LEFT JOIN customer_segments cs ON cs.client_id = cp.client_id
        ORDER BY cp.churn_probability DESC
        LIMIT :limit
    """)
    with engine.connect() as conn:
        rows = conn.execute(query, {"limit": limit}).mappings().all()
        return [dict(r) for r in rows]


def get_inactive_customers(limit: int = 100) -> list[dict]:
    """Customers with high inactivity — future churn watchlist."""
    engine = get_engine()
    query = text("SELECT * FROM v_inactive_customers LIMIT :limit")
    with engine.connect() as conn:
        rows = conn.execute(query, {"limit": limit}).mappings().all()
        return [dict(r) for r in rows]


def get_customer_health_distribution() -> list[dict]:
    """Health score distribution from ML predictions."""
    engine = get_engine()
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT * FROM v_customer_health_distribution")).mappings().all()
        return [dict(r) for r in rows]


def get_transaction_summary() -> list[dict]:
    """Transaction summary by category for spending analysis."""
    engine = get_engine()
    query = text("""
        SELECT
            category,
            COUNT(*) AS transaction_count,
            ROUND(AVG(amount)::numeric, 2) AS avg_amount,
            ROUND(SUM(amount)::numeric, 2) AS total_amount
        FROM transactions
        WHERE category IS NOT NULL
        GROUP BY category
        ORDER BY total_amount DESC
        LIMIT 15
    """)
    with engine.connect() as conn:
        rows = conn.execute(query).mappings().all()
        return [dict(r) for r in rows]

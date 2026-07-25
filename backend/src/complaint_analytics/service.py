"""
FinSight AI — Complaint Analytics Service Layer.

Business Context:
    Complaint analytics answers: "What are customers complaining about,
    how fast are we responding, and what is the sentiment?" This drives
    CX improvement, product fixes, and regulatory compliance.
"""

import logging
from sqlalchemy import text
from src.database.engine import get_engine

logger = logging.getLogger(__name__)


def get_complaint_kpis() -> dict:
    """Core complaint KPIs for the dashboard header."""
    engine = get_engine()
    with engine.connect() as conn:
        total = conn.execute(text("SELECT COUNT(*) AS cnt FROM complaints")).scalar()

        timely_row = conn.execute(text("SELECT * FROM v_timely_response_rate")).mappings().first()
        timely_pct = float(timely_row["timely_response_pct"]) if timely_row else 0

        res_row = conn.execute(text("SELECT * FROM v_avg_resolution_time")).mappings().first()
        avg_resolution = float(res_row["avg_resolution_days"]) if res_row and res_row["avg_resolution_days"] else 0

        growth_row = conn.execute(text("SELECT * FROM v_complaint_growth")).mappings().first()
        growth_pct = float(growth_row["growth_pct"]) if growth_row and growth_row["growth_pct"] else 0

        neg_row = conn.execute(text("SELECT * FROM v_negative_sentiment_pct")).mappings().first()
        neg_pct = float(neg_row["negative_pct"]) if neg_row and neg_row["negative_pct"] else 0

    return {
        "total_complaints": total,
        "timely_response_pct": timely_pct,
        "avg_resolution_days": avg_resolution,
        "complaint_growth_pct": growth_pct,
        "negative_sentiment_pct": neg_pct,
    }


def get_monthly_trends() -> list[dict]:
    """Monthly complaint volume trend."""
    engine = get_engine()
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT * FROM v_monthly_complaints")).mappings().all()
        return [dict(r) for r in rows]


def get_complaints_by_product() -> list[dict]:
    """Complaint distribution by product."""
    engine = get_engine()
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT * FROM v_complaints_by_product")).mappings().all()
        return [dict(r) for r in rows]


def get_complaints_by_issue() -> list[dict]:
    """Top complaint issues."""
    engine = get_engine()
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT * FROM v_complaints_by_issue")).mappings().all()
        return [dict(r) for r in rows]


def get_complaints_by_state() -> list[dict]:
    """State-wise complaint distribution."""
    engine = get_engine()
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT * FROM v_complaints_by_state")).mappings().all()
        return [dict(r) for r in rows]


def get_sentiment_distribution() -> list[dict]:
    """VADER sentiment label distribution."""
    engine = get_engine()
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT * FROM v_sentiment_distribution")).mappings().all()
        return [dict(r) for r in rows]


def get_sentiment_by_product() -> list[dict]:
    """Sentiment breakdown per product."""
    engine = get_engine()
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT * FROM v_sentiment_by_product")).mappings().all()
        return [dict(r) for r in rows]


def get_company_response_distribution() -> list[dict]:
    """How the company responded to complaints."""
    engine = get_engine()
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT * FROM v_company_response_distribution")).mappings().all()
        return [dict(r) for r in rows]


def get_word_frequency(limit: int = 50) -> list[dict]:
    """Top words in complaint narratives for word cloud.
    Computed server-side to avoid sending raw text to frontend.
    """
    engine = get_engine()
    import re
    from collections import Counter

    query = text("""
        SELECT narrative FROM complaints
        WHERE narrative IS NOT NULL AND narrative != ''
        LIMIT 10000
    """)
    with engine.connect() as conn:
        rows = conn.execute(query).all()

    # Simple word frequency (stopwords removed)
    stopwords = {
        "the", "a", "an", "is", "was", "were", "are", "be", "been", "being",
        "have", "has", "had", "do", "does", "did", "will", "would", "could",
        "should", "may", "might", "shall", "can", "need", "dare", "ought",
        "and", "but", "or", "nor", "not", "so", "yet", "both", "either",
        "neither", "each", "every", "all", "any", "few", "more", "most",
        "other", "some", "such", "no", "only", "own", "same", "than",
        "too", "very", "just", "because", "as", "until", "while", "of",
        "at", "by", "for", "with", "about", "against", "between", "through",
        "during", "before", "after", "above", "below", "to", "from", "up",
        "down", "in", "out", "on", "off", "over", "under", "again",
        "further", "then", "once", "i", "my", "me", "we", "our", "you",
        "your", "he", "him", "she", "her", "it", "its", "they", "them",
        "their", "this", "that", "these", "those", "what", "which", "who",
        "whom", "when", "where", "why", "how", "if", "also", "told",
    }

    counter = Counter()
    for row in rows:
        text_val = row[0] or ""
        words = re.findall(r"[a-z]+", text_val.lower())
        counter.update(w for w in words if w not in stopwords and len(w) > 2)

    return [{"word": w, "count": c} for w, c in counter.most_common(limit)]

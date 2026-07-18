"""FinSight AI — Dashboard Data Providers.

Backend data aggregation layer for Streamlit dashboard pages.
"""

import pandas as pd
from pathlib import Path

from src.common.logger import get_logger
from src.common.constants import PROCESSED_DIR

logger = get_logger(__name__)


def get_executive_metrics() -> dict:
    """Aggregate metrics across all modules for executive dashboard.

    Returns:
        Dictionary of executive-level KPIs.
    """
    metrics = {}

    # Customer metrics
    try:
        df = pd.read_csv(PROCESSED_DIR / "unified_customer_profile.csv")
        metrics["total_customers"] = len(df)
        if "churn_probability" in df.columns:
            metrics["avg_churn_risk"] = round(df["churn_probability"].mean(), 4)
        if "segment_name" in df.columns:
            metrics["segment_count"] = df["segment_name"].nunique()
    except Exception as e:
        logger.warning(f"Customer metrics unavailable: {e}")

    # Compliance metrics
    try:
        kyc = pd.read_csv(PROCESSED_DIR / "kyc_clean.csv")
        metrics["total_entities_monitored"] = len(kyc)
    except Exception as e:
        logger.warning(f"Compliance metrics unavailable: {e}")

    # Complaint metrics
    try:
        comp = pd.read_csv(PROCESSED_DIR / "complaints_with_escalation.csv")
        metrics["total_complaints"] = len(comp)
    except Exception as e:
        logger.warning(f"Complaint metrics unavailable: {e}")

    return metrics

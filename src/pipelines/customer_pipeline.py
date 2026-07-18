"""FinSight AI — Customer Intelligence Pipeline.

Orchestrates the full customer analytics workflow:
Segmentation → Inactivity Scoring → Churn Prediction → Unified Profile.
"""

from pathlib import Path
from typing import Optional

import pandas as pd

from src.common.logger import get_logger
from src.common.constants import PROCESSED_DIR

logger = get_logger(__name__)


def run_customer_pipeline(output_dir: Optional[Path] = None) -> dict:
    """Execute the full customer intelligence pipeline.

    Args:
        output_dir: Directory to save outputs. Defaults to data/processed/.

    Returns:
        Dictionary with pipeline execution summary.
    """
    output_dir = output_dir or PROCESSED_DIR
    results = {}

    # Step 1: Load base customer data
    logger.info("Step 1/4: Loading customer data")
    customer_path = output_dir / "customer_clean.csv"
    if not customer_path.exists():
        logger.error(f"Customer data not found at {customer_path}")
        return {"status": "error", "message": "customer_clean.csv not found"}
    df = pd.read_csv(customer_path)
    results["total_customers"] = len(df)

    # Step 2: Apply segmentation
    logger.info("Step 2/4: Applying K-Means segmentation")
    try:
        from src.customer_intelligence.segmentation import get_segment_distribution
        results["segments"] = get_segment_distribution()
    except Exception as e:
        logger.warning(f"Segmentation failed: {e}")
        results["segments"] = "skipped"

    # Step 3: Score inactivity
    logger.info("Step 3/4: Scoring customer inactivity")
    try:
        from src.customer_intelligence.inactivity import get_activity_distribution
        results["activity"] = get_activity_distribution()
    except Exception as e:
        logger.warning(f"Inactivity scoring failed: {e}")
        results["activity"] = "skipped"

    # Step 4: Predict churn
    logger.info("Step 4/4: Predicting customer churn")
    try:
        from src.customer_intelligence.churn import get_churn_distribution
        results["churn"] = get_churn_distribution()
    except Exception as e:
        logger.warning(f"Churn prediction failed: {e}")
        results["churn"] = "skipped"

    results["status"] = "completed"
    logger.info("Customer pipeline completed successfully")
    return results

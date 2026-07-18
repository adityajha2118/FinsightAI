"""FinSight AI — Master Pipeline Orchestrator.

Ties all domain-specific pipelines into a unified DAG for batch execution.
"""

from src.common.logger import get_logger
from src.pipelines.customer_pipeline import run_customer_pipeline
from src.pipelines.campaign_pipeline import run_campaign_pipeline
from src.pipelines.compliance_pipeline import run_compliance_pipeline

logger = get_logger(__name__)


def run_all_pipelines() -> dict:
    """Execute all analytics pipelines in dependency order.

    Execution order:
    1. Customer Intelligence (segmentation, inactivity, churn)
    2. Campaign Analytics
    3. Compliance / KYC
    4. Complaint Intelligence (on-demand only, not batch)

    Returns:
        Aggregated results from all pipelines.
    """
    logger.info("=" * 60)
    logger.info("Starting FinSight AI Master Pipeline")
    logger.info("=" * 60)

    results = {}

    # Pipeline 1: Customer Intelligence
    logger.info("[1/3] Customer Intelligence Pipeline")
    results["customer"] = run_customer_pipeline()

    # Pipeline 2: Campaign Analytics
    logger.info("[2/3] Campaign Analytics Pipeline")
    results["campaign"] = run_campaign_pipeline()

    # Pipeline 3: Compliance
    logger.info("[3/3] Compliance Pipeline")
    results["compliance"] = run_compliance_pipeline()

    # Note: Complaint pipeline is on-demand (per-request), not batch
    results["complaint"] = {"status": "on-demand", "note": "Triggered per API request"}

    logger.info("=" * 60)
    logger.info("Master Pipeline Complete")
    logger.info("=" * 60)

    return results


if __name__ == "__main__":
    results = run_all_pipelines()
    for domain, result in results.items():
        print(f"  {domain}: {result.get('status', 'unknown')}")

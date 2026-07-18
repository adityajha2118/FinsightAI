"""FinSight AI — Compliance Analytics Pipeline."""

from src.common.logger import get_logger

logger = get_logger(__name__)


def run_compliance_pipeline() -> dict:
    """Execute KYC/AML compliance pipeline.

    Returns:
        Pipeline execution summary.
    """
    logger.info("Starting compliance pipeline")
    try:
        from src.compliance.kyc_prediction import get_risk_distribution
        distribution = get_risk_distribution()
        logger.info("Compliance pipeline completed")
        return {"status": "completed", "risk_distribution": distribution}
    except Exception as e:
        logger.error(f"Compliance pipeline failed: {e}")
        return {"status": "error", "message": str(e)}

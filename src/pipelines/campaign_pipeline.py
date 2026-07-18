"""FinSight AI — Campaign Analytics Pipeline."""

from src.common.logger import get_logger

logger = get_logger(__name__)


def run_campaign_pipeline() -> dict:
    """Execute campaign analytics pipeline.

    Returns:
        Pipeline execution summary.
    """
    logger.info("Starting campaign pipeline")
    try:
        from src.campaign_analytics.campaign_analysis import get_full_campaign_stats
        stats = get_full_campaign_stats()
        logger.info("Campaign pipeline completed")
        return {"status": "completed", "stats": stats}
    except Exception as e:
        logger.error(f"Campaign pipeline failed: {e}")
        return {"status": "error", "message": str(e)}

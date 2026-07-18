"""FinSight AI — Complaint Intelligence Pipeline."""

from src.common.logger import get_logger

logger = get_logger(__name__)


def run_complaint_pipeline(narrative: str) -> dict:
    """Execute complaint processing pipeline via LangGraph agent.

    Args:
        narrative: Raw customer complaint text.

    Returns:
        Complete agent state with analysis results.
    """
    logger.info("Starting complaint pipeline")
    try:
        from src.agents.complaint_agent import run_complaint_agent
        result = run_complaint_agent(narrative)
        logger.info(f"Complaint processed — Priority: {result.get('priority_level')}")
        return result
    except Exception as e:
        logger.error(f"Complaint pipeline failed: {e}")
        return {"status": "error", "message": str(e)}

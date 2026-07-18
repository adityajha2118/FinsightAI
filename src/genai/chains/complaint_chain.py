"""FinSight AI — Complaint Processing LangChain Chain."""

import os
from typing import Optional

from src.common.logger import get_logger

logger = get_logger(__name__)


def get_llm(provider: Optional[str] = None):
    """Get the configured LLM client based on provider setting.

    Args:
        provider: LLM provider ("gemini" or "openai"). Defaults to env var.

    Returns:
        LangChain chat model instance.
    """
    provider = provider or os.getenv("LLM_PROVIDER", "gemini")

    if provider == "gemini":
        from src.genai.llm_clients.gemini_client import get_gemini_client
        return get_gemini_client()
    else:
        from src.genai.llm_clients.openai_client import get_openai_client
        return get_openai_client()


def run_complaint_chain(narrative: str) -> dict:
    """Run the full complaint analysis chain.

    Args:
        narrative: Raw complaint text.

    Returns:
        Dictionary with summary, category, and emotion.
    """
    from src.genai.prompts.complaint_prompts import (
        SUMMARIZE_PROMPT, CLASSIFY_PROMPT, EMOTION_PROMPT
    )

    llm = get_llm()
    results = {}

    try:
        results["summary"] = llm.invoke(
            SUMMARIZE_PROMPT.format(narrative=narrative)
        ).content.strip()
    except Exception as e:
        logger.warning(f"Summarization failed: {e}")
        results["summary"] = "Summary unavailable"

    try:
        results["category"] = llm.invoke(
            CLASSIFY_PROMPT.format(narrative=narrative)
        ).content.strip()
    except Exception as e:
        logger.warning(f"Classification failed: {e}")
        results["category"] = "Other"

    try:
        results["emotion"] = llm.invoke(
            EMOTION_PROMPT.format(narrative=narrative)
        ).content.strip()
    except Exception as e:
        logger.warning(f"Emotion detection failed: {e}")
        results["emotion"] = "Neutral"

    return results

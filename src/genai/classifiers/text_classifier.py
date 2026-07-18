"""FinSight AI — Generic Text Classifier."""

from typing import List

from src.common.logger import get_logger

logger = get_logger(__name__)


def classify_text(text: str, categories: List[str]) -> str:
    """Classify text into one of the provided categories using LLM.

    Args:
        text: Input text to classify.
        categories: List of valid category labels.

    Returns:
        Predicted category label.
    """
    from src.genai.chains.complaint_chain import get_llm

    cats = ", ".join(categories)
    prompt = f"Classify this text into one of: {cats}\n\nText: {text}\n\nCategory:"

    try:
        llm = get_llm()
        result = llm.invoke(prompt).content.strip()
        # Validate against known categories
        for cat in categories:
            if cat.lower() in result.lower():
                return cat
        return categories[-1]  # Default to last category (usually "Other")
    except Exception as e:
        logger.warning(f"Classification failed: {e}")
        return categories[-1]

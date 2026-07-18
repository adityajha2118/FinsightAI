"""FinSight AI — Generic Text Summarizer."""

from src.common.logger import get_logger

logger = get_logger(__name__)


def summarize_text(text: str, max_sentences: int = 2) -> str:
    """Summarize text using the configured LLM.

    Args:
        text: Input text to summarize.
        max_sentences: Maximum number of sentences in summary.

    Returns:
        Summarized text string.
    """
    from src.genai.chains.complaint_chain import get_llm

    prompt = f"Summarize the following text in {max_sentences} sentences:\n\n{text}\n\nSummary:"

    try:
        llm = get_llm()
        return llm.invoke(prompt).content.strip()
    except Exception as e:
        logger.warning(f"Summarization failed: {e}")
        return text[:200] + "..." if len(text) > 200 else text

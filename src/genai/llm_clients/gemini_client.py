"""FinSight AI — Gemini LLM Client Wrapper."""

import os
from typing import Optional

from src.common.logger import get_logger

logger = get_logger(__name__)


def get_gemini_client(
    model: str = "gemini-1.5-flash",
    temperature: float = 0.3,
):
    """Create a LangChain Gemini LLM client.

    Args:
        model: Gemini model name.
        temperature: Sampling temperature.

    Returns:
        ChatGoogleGenerativeAI instance.

    Raises:
        ValueError: If GOOGLE_API_KEY is not set.
    """
    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("GOOGLE_API_KEY environment variable not set")

    from langchain_google_genai import ChatGoogleGenerativeAI

    logger.info(f"Initializing Gemini client: {model} (temp={temperature})")
    return ChatGoogleGenerativeAI(model=model, temperature=temperature)


def invoke_gemini(prompt: str, model: Optional[str] = None) -> str:
    """Send a prompt to Gemini and return the response text.

    Args:
        prompt: The prompt string.
        model: Optional model override.

    Returns:
        Response text content.
    """
    client = get_gemini_client(model=model or "gemini-1.5-flash")
    response = client.invoke(prompt)
    return response.content.strip()

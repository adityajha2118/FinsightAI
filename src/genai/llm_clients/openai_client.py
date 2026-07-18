"""FinSight AI — OpenAI LLM Client Wrapper."""

import os
from typing import Optional

from src.common.logger import get_logger

logger = get_logger(__name__)


def get_openai_client(
    model: str = "gpt-4o-mini",
    temperature: float = 0.3,
):
    """Create a LangChain OpenAI LLM client.

    Args:
        model: OpenAI model name.
        temperature: Sampling temperature.

    Returns:
        ChatOpenAI instance.

    Raises:
        ValueError: If OPENAI_API_KEY is not set.
    """
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY environment variable not set")

    from langchain_openai import ChatOpenAI

    logger.info(f"Initializing OpenAI client: {model} (temp={temperature})")
    return ChatOpenAI(model=model, temperature=temperature)


def invoke_openai(prompt: str, model: Optional[str] = None) -> str:
    """Send a prompt to OpenAI and return the response text.

    Args:
        prompt: The prompt string.
        model: Optional model override.

    Returns:
        Response text content.
    """
    client = get_openai_client(model=model or "gpt-4o-mini")
    response = client.invoke(prompt)
    return response.content.strip()

"""FinSight AI — LLM Response Quality Evaluator."""

from src.common.logger import get_logger

logger = get_logger(__name__)


def evaluate_response(response: str, context: dict) -> dict:
    """Evaluate the quality of an LLM-generated response.

    Args:
        response: The generated response text.
        context: Dictionary with category, emotion, priority_level.

    Returns:
        Evaluation dictionary with quality metrics.
    """
    evaluation = {
        "length_adequate": 20 <= len(response) <= 500,
        "is_professional": not any(
            word in response.lower()
            for word in ["damn", "hell", "stupid", "idiot"]
        ),
        "mentions_resolution": any(
            word in response.lower()
            for word in ["resolve", "assist", "help", "address", "investigate"]
        ),
        "is_empathetic": any(
            word in response.lower()
            for word in ["understand", "apologize", "sorry", "concern", "appreciate"]
        ),
    }

    evaluation["quality_score"] = sum(evaluation.values()) / len(evaluation)
    return evaluation

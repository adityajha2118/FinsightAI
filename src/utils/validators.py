"""FinSight AI — Input Validation Helpers."""

from typing import Any


def validate_narrative(narrative: str, min_length: int = 20) -> str:
    """Validate complaint narrative text.

    Args:
        narrative: Raw complaint text.
        min_length: Minimum character length.

    Returns:
        Stripped narrative string.

    Raises:
        ValueError: If narrative is too short or empty.
    """
    if not narrative or not isinstance(narrative, str):
        raise ValueError("Narrative must be a non-empty string")

    cleaned = narrative.strip()
    if len(cleaned) < min_length:
        raise ValueError(f"Narrative must be at least {min_length} characters")

    return cleaned


def validate_features(features: dict[str, Any], required_keys: list[str]) -> dict:
    """Validate that all required feature keys are present.

    Args:
        features: Feature dictionary to validate.
        required_keys: List of required key names.

    Returns:
        Validated feature dictionary.

    Raises:
        ValueError: If required keys are missing.
    """
    missing = [k for k in required_keys if k not in features]
    if missing:
        raise ValueError(f"Missing required features: {missing}")

    return features

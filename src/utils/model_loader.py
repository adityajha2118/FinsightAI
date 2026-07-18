"""FinSight AI — Model Loading Utilities."""

from pathlib import Path
from typing import Any

import joblib

from src.common.logger import get_logger
from src.common.exceptions import ModelNotFoundError

logger = get_logger(__name__)

# Singleton cache for loaded models
_model_cache: dict[str, Any] = {}


def load_model(model_path: Path, use_cache: bool = True) -> Any:
    """Load a serialized model artifact with optional caching.

    Args:
        model_path: Path to the .pkl model file.
        use_cache: Whether to cache the model in memory.

    Returns:
        Deserialized model object.

    Raises:
        ModelNotFoundError: If the model file does not exist.
    """
    cache_key = str(model_path)

    if use_cache and cache_key in _model_cache:
        return _model_cache[cache_key]

    if not model_path.exists():
        raise ModelNotFoundError(str(model_path))

    logger.info(f"Loading model: {model_path}")
    model = joblib.load(model_path)

    if use_cache:
        _model_cache[cache_key] = model

    return model


def clear_model_cache() -> None:
    """Clear the in-memory model cache."""
    _model_cache.clear()
    logger.info("Model cache cleared")

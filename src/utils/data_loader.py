"""FinSight AI — Unified Data Loading Utilities."""

from pathlib import Path
from typing import Optional

import pandas as pd

from src.common.logger import get_logger
from src.common.constants import PROCESSED_DIR, FEATURE_STORE_DIR
from src.common.exceptions import DataNotFoundError

logger = get_logger(__name__)

# Cache loaded DataFrames to avoid redundant disk I/O
_cache: dict[str, pd.DataFrame] = {}


def load_csv(filename: str, directory: Optional[Path] = None, use_cache: bool = True) -> pd.DataFrame:
    """Load a CSV file with optional caching.

    Args:
        filename: Name of the CSV file.
        directory: Directory containing the file. Defaults to processed/.
        use_cache: Whether to cache the DataFrame in memory.

    Returns:
        Loaded DataFrame.

    Raises:
        DataNotFoundError: If the file does not exist.
    """
    directory = directory or PROCESSED_DIR
    filepath = directory / filename
    cache_key = str(filepath)

    if use_cache and cache_key in _cache:
        return _cache[cache_key]

    if not filepath.exists():
        raise DataNotFoundError(str(filepath))

    logger.info(f"Loading {filepath}")
    df = pd.read_csv(filepath)

    if use_cache:
        _cache[cache_key] = df

    return df


def load_parquet(filename: str, directory: Optional[Path] = None) -> pd.DataFrame:
    """Load a Parquet file from the feature store.

    Args:
        filename: Name of the Parquet file.
        directory: Directory containing the file. Defaults to feature_store/.

    Returns:
        Loaded DataFrame.

    Raises:
        DataNotFoundError: If the file does not exist.
    """
    directory = directory or FEATURE_STORE_DIR
    filepath = directory / filename

    if not filepath.exists():
        raise DataNotFoundError(str(filepath))

    logger.info(f"Loading {filepath}")
    return pd.read_parquet(filepath)


def clear_cache() -> None:
    """Clear the in-memory data cache."""
    _cache.clear()
    logger.info("Data cache cleared")

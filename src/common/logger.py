"""FinSight AI — Centralized Logging Configuration."""

import logging
import sys


def get_logger(name: str, level: str = "INFO") -> logging.Logger:
    """Create a configured logger instance.

    Args:
        name: Logger name (typically __name__).
        level: Logging level string.

    Returns:
        Configured logging.Logger instance.
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(getattr(logging, level.upper(), logging.INFO))

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger

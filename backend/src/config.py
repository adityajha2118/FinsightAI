"""
FinSight AI — Application Configuration.

Centralizes all environment-based settings. No hardcoded paths or credentials.
Uses pydantic-settings for validation and type coercion.
"""

import os
from pathlib import Path
from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # ── Database ─────────────────────────────────────────────
    database_url: str = "postgresql://postgres:postgres@localhost:5432/finsight"

    # ── Paths ────────────────────────────────────────────────
    project_root: Path = Path(__file__).resolve().parent.parent
    models_dir: Path = Path(__file__).resolve().parent.parent / "models"
    data_dir: Path = Path(__file__).resolve().parent.parent.parent / "data"

    # ── API ──────────────────────────────────────────────────
    api_title: str = "FinSight AI"
    api_description: str = "Enterprise Customer Analytics & Decision Intelligence Platform"
    api_version: str = "2.0.0"
    cors_origins: list[str] = ["*"]

    # ── ML ───────────────────────────────────────────────────
    churn_threshold: float = 0.7
    risk_critical_threshold: float = 0.75
    risk_high_threshold: float = 0.50
    risk_medium_threshold: float = 0.25

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    """Return cached settings instance. Call once at startup."""
    return Settings()

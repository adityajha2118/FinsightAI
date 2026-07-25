"""
FinSight AI — Database Engine & Session Management.

Provides the SQLAlchemy engine, session factory, and Base class.
PostgreSQL is the single source of truth for all analytics data.

Usage:
    from src.database.engine import get_engine, get_session, Base

    # In FastAPI dependency injection:
    def get_db():
        db = get_session()
        try:
            yield db
        finally:
            db.close()
"""

import logging
from contextlib import contextmanager

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base, Session

from src.config import get_settings

logger = logging.getLogger(__name__)

# ── Engine & Session Factory ──────────────────────────────────
_engine = None
_SessionLocal = None
Base = declarative_base()


def get_engine():
    """Return the singleton SQLAlchemy engine."""
    global _engine
    if _engine is None:
        settings = get_settings()
        _engine = create_engine(
            settings.database_url,
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True,
            echo=False,
        )
        logger.info("Database engine created: %s", settings.database_url.split("@")[-1])
    return _engine


def get_session_factory():
    """Return the sessionmaker bound to the engine."""
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=get_engine(),
        )
    return _SessionLocal


def get_session() -> Session:
    """Create a new database session."""
    factory = get_session_factory()
    return factory()


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations.

    Usage:
        with session_scope() as session:
            session.execute(text("SELECT 1"))
    """
    session = get_session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_db():
    """FastAPI dependency that provides a database session per request."""
    db = get_session()
    try:
        yield db
    finally:
        db.close()


def check_connection() -> bool:
    """Verify the database is reachable. Returns True if healthy."""
    try:
        engine = get_engine()
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.error("Database connection check failed: %s", e)
        return False

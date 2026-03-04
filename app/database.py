# app/database.py
"""
Database configuration and connection for FastAPI + SQLAlchemy.

- Creates the SQLAlchemy engine
- Provides a session factory (SessionLocal)
- Defines the declarative base class for models
- Provides a FastAPI dependency for DB sessions
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

# -------------------------------
# SQLAlchemy Engine
# -------------------------------
# The engine is the starting point for any SQLAlchemy application.
# `connect_args={"check_same_thread": False}` is required only for SQLite.
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {},
)

# -------------------------------
# Session factory
# -------------------------------
# SessionLocal is a factory to create new Session objects.
# autocommit=False → explicit commit is required (recommended)
# autoflush=False → avoids automatic flush before queries (safer for FastAPI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# -------------------------------
# Base class for models
# -------------------------------
# All SQLAlchemy ORM models should inherit from this Base.
Base = declarative_base()

# -------------------------------
# FastAPI Dependency
# -------------------------------
def get_db():
    """
    FastAPI dependency to provide a database session per request.
    Yields:
        Session: SQLAlchemy database session
    Usage:
        @app.get("/items/")
        def read_items(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
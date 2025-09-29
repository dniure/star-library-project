"""
database.py
-------------------
Manages the SQLAlchemy database engine, session factory, and core utilities
for connection lifecycle and dependency injection.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

# Constants
SQLALCHEMY_DATABASE_URL = "sqlite:///./starlibrary.db"

# Engine & Session Setup
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # Required for SQLite to run concurrently with FastAPI threads
    connect_args={"check_same_thread": False}
)

# Session Factory: Used to create new, isolated sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Helper Functions
def create_tables():
    """Create all database tables defined in models using the engine."""
    # Base.metadata contains the blueprint for all models
    Base.metadata.create_all(bind=engine)


def get_db():
    """
    Dependency for FastAPI routes.
    Provides a database session and ensures proper cleanup using a generator pattern.
    """
    db = SessionLocal()
    try:
        # Yields the session to the FastAPI route
        yield db
    finally:
        # Ensures the session is closed after the request is finished or errors out
        db.close()
"""
Database Configuration
SQLAlchemy engine, session management, and connection utilities.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

# Database Configuration
SQLALCHEMY_DATABASE_URL = "sqlite:///./starlibrary.db"

# Database engine with SQLite connection optimization
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # Required for SQLite thread safety
)

# Session factory for creating database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    """Initialize database schema by creating all defined tables."""
    Base.metadata.create_all(bind=engine)

def get_db():
    """
    Database session dependency for FastAPI route injection.
    
    Yields:
        Database session for request processing
        
    Ensures:
        Session is properly closed after request completion
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
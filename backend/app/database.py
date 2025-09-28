from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

# --- Constants ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./starlibrary.db"  # Could later move to env variable

# --- Engine & Session ---
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # SQLite specific
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# --- Helper Functions ---
def create_tables():
    """Create all database tables defined in models."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """
    Dependency for FastAPI routes.
    Provides a database session and ensures proper cleanup.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

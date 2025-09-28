# backend/tests/conftest.py (Final Robust Version)

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator
from datetime import datetime, timezone
import sys
import os

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.database import Base, get_db
from app.api import app
from app import models

# -------------------------------
# Create an in-memory SQLite DB
# -------------------------------
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    # Use a separate connection argument specific to in-memory testing
    connect_args={"check_same_thread": False}
)

# -------------------------------
# Engine and Connection Fixture
# -------------------------------
@pytest.fixture(scope="session")
def db_engine():
    """Provides a single, persistent connection for the entire test session."""
    # Start a separate connection to keep the in-memory DB alive
    connection = engine.connect()
    yield connection
    connection.close()
    # Note: DB is technically dropped here as the last connection closes

# -------------------------------
# Database Fixture: Create/Seed/Teardown
# -------------------------------
# Change scope to 'function' so each test gets a fresh, isolated session/data
@pytest.fixture(scope="function")
def db(db_engine) -> Generator:
    """
    Creates tables, seeds data, yields a new test session bound to the persistent connection.
    """
    
    # 1. BIND SESSION MAKER to the persistent connection
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    
    # 2. CREATE TABLES (MUST BE BOUND TO THE PERSISTENT CONNECTION)
    Base.metadata.create_all(bind=db_engine)
    
    # 3. Create a session 
    db = TestingSessionLocal()
    
    try:
        # 4. Seed Data (Same data as before, ensures data for API calls)
        author1 = models.Author(id=1, name="J.K. Rowling", bio="Fantasy writer", nationality="British")
        author2 = models.Author(id=2, name="George Orwell", bio="Dystopian writer", nationality="British")
        reader1 = models.Reader(id=1, name="Alice", email="alice@example.com", 
                                join_date=datetime.now(timezone.utc), favorite_genre="Fantasy")
        # Use 9999 as the non-existent ID for testing 404s
        reader9999 = models.Reader(id=9999, name="Bob", email="bob@example.com", 
                                  join_date=datetime.now(timezone.utc), favorite_genre="Dystopian")
        book1 = models.Book(id=1, title="HP and the Sorcerer's Stone", genre="Fantasy", 
                            pages=320, published_year=1997, rating=4.5, author_id=author1.id, 
                            readers_count=1, description="A young wizard's journey begins")
        book2 = models.Book(id=2, title="1984", genre="Dystopian", pages=328, 
                            published_year=1949, rating=4.7, author_id=author2.id, 
                            readers_count=0, description="A dystopian social science fiction novel")
        
        db.add_all([author1, author2, reader1, reader9999, book1, book2])
        db.flush() 

        reader1.books_read.append(book1)
        
        db.commit()

        # 5. Yield the populated session to tests
        yield db
        
    finally:
        # 6. Teardown: Close the session and clear the tables for the next test
        db.close()
        # Drop all tables after each test to ensure a clean state
        Base.metadata.drop_all(bind=db_engine)


# -------------------------------
# FastAPI test client fixture
# -------------------------------
@pytest.fixture(scope="function")
def client(db) -> Generator[TestClient, None, None]:
    """
    Provides a configured TestClient with the mocked database dependency.
    """
    
    def override_get_db():
        # Yield the same session object created by the 'db' fixture
        try:
            yield db
        finally:
            pass 

    # Override the dependency
    app.dependency_overrides[get_db] = override_get_db
    
    # Use TestClient without lifespan argument (since it's not supported)
    with TestClient(app) as test_client: 
        yield test_client
    
    # Clear the overrides after the test
    app.dependency_overrides.clear()
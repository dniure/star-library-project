# backend/tests/conftest.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator
from datetime import datetime, timezone
import sys
import os

# -------------------------------
# Ensure app directory is on path
# -------------------------------
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.database import Base, get_db
from app.api import app
from app import models

# -------------------------------
# Create in-memory SQLite DB
# -------------------------------
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# -------------------------------
# Engine and Connection Fixture
# -------------------------------
@pytest.fixture(scope="session")
def db_engine():
    """Provides a persistent DB connection for the whole test session."""
    connection = engine.connect()
    yield connection
    connection.close()

# -------------------------------
# Database Fixture (Create/Seed/Teardown)
# -------------------------------
@pytest.fixture(scope="function")
def db(db_engine) -> Generator:
    """Provides a fresh DB session with seeded data per test."""
    
    # 1. Bind sessionmaker to persistent engine
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)

    # 2. Create tables
    Base.metadata.create_all(bind=db_engine)

    # 3. Create a session
    db = TestingSessionLocal()
    try:
        # 4. Seed initial test data
        author1 = models.Author(id=1, name="J.K. Rowling", bio="Fantasy writer", nationality="British")
        author2 = models.Author(id=2, name="George Orwell", bio="Dystopian writer", nationality="British")
        reader1 = models.Reader(id=1, name="Alice", email="alice@example.com",
                                join_date=datetime.now(timezone.utc), favorite_genre="Fantasy")
        reader9999 = models.Reader(id=9999, name="Bob", email="bob@example.com",
                                   join_date=datetime.now(timezone.utc), favorite_genre="Dystopian")
        book1 = models.Book(id=1, title="HP and the Sorcerer's Stone", genre="Fantasy",
                            pages=320, published_year=1997, rating=4.5, author_id=author1.id,
                            readers_count=1, description="A young wizard's journey begins")
        book2 = models.Book(id=2, title="1984", genre="Dystopian", pages=328,
                            published_year=1949, rating=4.7, author_id=author2.id,
                            readers_count=0, description="A dystopian novel")

        db.add_all([author1, author2, reader1, reader9999, book1, book2])
        db.flush()
        reader1.books_read.append(book1)
        db.commit()

        # 5. Yield ready session
        yield db

    finally:
        # 6. Teardown DB
        db.close()
        Base.metadata.drop_all(bind=db_engine)

# -------------------------------
# FastAPI Test Client Fixture
# -------------------------------
@pytest.fixture(scope="function")
def client(db) -> Generator[TestClient, None, None]:
    """Provides TestClient with test DB overrides."""

    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()

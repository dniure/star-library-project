"""
FastAPI Application Configuration
Primary application file defining API routes, middleware, and lifecycle management.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List
import logging

from ..database import get_db, create_tables
from .. import schemas, crud, models
from ..seed import seed_database

# Configuration
logger = logging.getLogger(__name__)
HARDCODED_READER_ID = 1  # Temporary authentication simulation

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle manager for startup/shutdown events."""
    logger.info("Starting STAR Library API...")
    
    # Initialize database in non-testing environments
    if not __import__('os').getenv("TESTING_ENV"):
        try:
            create_tables()
            seed_database()
            logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            raise
    
    yield  # Application runs here
    
    logger.info("Shutting down STAR Library API...")

# FastAPI Application Instance
app = FastAPI(
    title="STAR Library API",
    version="1.0.0",
    description="REST API for library management with books, authors, and readers",
    lifespan=lifespan
)

# CORS Configuration for Frontend Integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React development server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_current_user(db: Session = Depends(get_db)) -> models.Reader:
    """Retrieve current user for authentication (simulated with hardcoded ID)."""
    reader = crud.get_reader_with_stats(db, HARDCODED_READER_ID)
    if not reader:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reader not found. Please seed the database."
        )
    return reader

# API Endpoints
@app.get("/", tags=["Root"], response_model=dict)
async def root():
    """API health and information endpoint."""
    return {
        "message": "STAR Library API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health", tags=["Root"], response_model=dict)
async def health_check(db: Session = Depends(get_db)):
    """Database connectivity health check."""
    try:
        db.execute("SELECT 1")  # Simple connection test
        db_status = "connected"
    except SQLAlchemyError as e:
        logger.error(f"Database health check failed: {e}")
        db_status = "disconnected"
    
    return {
        "status": "healthy",
        "database": db_status
    }

@app.get(
    "/dashboardData",
    response_model=schemas.DashboardData,
    tags=["Dashboard"],
    summary="Get reader dashboard data",
    description="Retrieve personalized dashboard with reading statistics and recommendations."
)
async def get_dashboard(
    current_reader: models.Reader = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Fetch comprehensive dashboard data for authenticated reader."""
    try:
        return schemas.DashboardData(
            reader_id=current_reader.id,
            reader_name=current_reader.name,
            most_popular_books=crud.get_most_popular_books(db),
            most_popular_author=crud.get_most_popular_author(db),
            user_books_read=current_reader.books_read,
            user_top_authors=crud.get_reader_top_authors(db, current_reader.id)
        )
    except Exception as e:
        logger.error(f"Dashboard error for reader {current_reader.id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching dashboard data"
        )

@app.get("/books/", response_model=List[schemas.Book], tags=["Books"])
async def get_books(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Retrieve paginated books with author information and reader statistics."""
    # Validate pagination parameters
    if skip < 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Skip parameter cannot be negative"
        )
    if not 0 < limit <= 1000:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Limit must be between 1 and 1000"
        )
    
    return crud.get_books(db, skip=skip, limit=limit)

@app.get("/authors/", response_model=List[schemas.Author], tags=["Authors"])
async def get_authors(db: Session = Depends(get_db)):
    """Retrieve all authors with book counts and reader statistics."""
    return crud.get_authors(db)

# Exception Handlers
@app.exception_handler(SQLAlchemyError)
async def handle_database_error(request, exc):
    """Handle database-related exceptions with consistent error response."""
    logger.error(f"Database error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Database error occurred"}
    )

@app.exception_handler(Exception)
async def handle_generic_error(request, exc):
    """Handle unexpected exceptions with logging and safe response."""
    logger.error(f"Unexpected error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"}
    )

# OpenAPI Documentation Configuration
app.openapi_tags = [
    {"name": "Root", "description": "API health and information endpoints"},
    {"name": "Dashboard", "description": "Personalized reader dashboard endpoints"},
    {"name": "Books", "description": "Book management and retrieval operations"},
    {"name": "Authors", "description": "Author information and statistics"},
]
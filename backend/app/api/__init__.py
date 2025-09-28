# backend/app/api/__init__.py

from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from os import environ
from typing import List
import logging

from ..database import get_db, create_tables
from .. import schemas, crud, models
from ..seed import seed_database

# Configure logging
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for application startup and shutdown events.
    Replaces the deprecated @app.on_event decorator.
    """
    # Startup
    logger.info("Starting up STAR Library API...")
    if environ.get("TESTING_ENV") != "True":
        try:
            create_tables()
            seed_database()
            logger.info("✅ Database initialized successfully")
        except Exception as e:
            logger.error(f"❌ Database initialization failed: {e}")
            raise
    else:
        logger.info("Skipping production DB setup in TESTING_ENV.")
   
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down STAR Library API...")

app = FastAPI(
    title="STAR Library API", 
    version="1.0.0",
    description="A REST API for managing library books, authors, and readers",
    lifespan=lifespan
)

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# --- Root & Health Check ---
@app.get("/", tags=["Root"], response_model=dict)
def read_root():
    """Root endpoint returning API information."""
    return {
        "message": "STAR Library API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health", tags=["Root"], response_model=dict)
def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint to verify API and database connectivity.
    """
    try:
        # Test database connection
        db.execute("SELECT 1")
        db_status = "connected"
    except SQLAlchemyError as e:
        logger.error(f"Database health check failed: {e}")
        db_status = "disconnected"
    
    return {
        "status": "healthy", 
        "database": db_status,
        "timestamp": "2024-01-01T00:00:00Z"  # You might want to use actual timestamp
    }

# --- Dashboard Route ---
@app.get(
    "/dashboard/{reader_id}", 
    response_model=schemas.DashboardStats, 
    tags=["Dashboard"],
    summary="Get reader dashboard",
    description="Fetch comprehensive dashboard statistics for a specific reader including popular books and reading insights."
)
def get_dashboard(reader_id: int, db: Session = Depends(get_db)):
    """Fetch dashboard stats for a reader."""
    # Validate reader_id
    if reader_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Reader ID must be a positive integer"
        )
    
    reader = crud.get_reader_by_id(db, reader_id)
    if not reader:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reader with ID {reader_id} not found"
        )

    try:
        most_popular_books = crud.get_most_popular_books(db)
        top_authors = crud.get_reader_top_authors(db, reader_id)
        
        most_popular_author = top_authors[0] if top_authors else None

        return schemas.DashboardStats(
            reader_id=reader.id,
            most_popular_books=most_popular_books,
            most_popular_author=most_popular_author,
            books_read=reader.books_read,
            user_top_authors=top_authors
        )
    except Exception as e:
        logger.error(f"Error fetching dashboard for reader {reader_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while fetching dashboard data"
        )

# --- Books Endpoint ---
@app.get(
    "/books/", 
    response_model=List[schemas.Book], 
    tags=["Books"],
    summary="Get all books",
    description="Fetch paginated list of books with author information and reader counts."
)
def get_books(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """Fetch paginated books with author and readers info."""
    # Validate pagination parameters
    if skip < 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Skip parameter cannot be negative"
        )
    
    if limit <= 0 or limit > 1000:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Limit must be between 1 and 1000"
        )
    
    try:
        return crud.get_books(db, skip=skip, limit=limit)
    except Exception as e:
        logger.error(f"Error fetching books (skip={skip}, limit={limit}): {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while fetching books"
        )

# --- Authors Endpoint ---
@app.get(
    "/authors/", 
    response_model=List[schemas.Author], 
    tags=["Authors"],
    summary="Get all authors",
    description="Fetch all authors with their book counts and total reader statistics."
)
def get_authors(db: Session = Depends(get_db)):
    """Fetch all authors with their books and total readers."""
    try:
        return crud.get_authors(db)
    except Exception as e:
        logger.error(f"Error fetching authors: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while fetching authors"
        )

# --- Reader Endpoint ---
@app.get(
    "/readers/{reader_id}", 
    response_model=schemas.Reader, 
    tags=["Readers"],
    summary="Get reader by ID",
    description="Fetch detailed information about a specific reader including their reading history."
)
def get_reader(reader_id: int, db: Session = Depends(get_db)):
    """Fetch reader info along with books read count."""
    # Validate reader_id
    if reader_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Reader ID must be a positive integer"
        )
    
    reader = crud.get_reader_with_stats(db, reader_id)
    if not reader:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reader with ID {reader_id} not found"
        )
    
    return reader

# --- Exception Handlers ---
@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request, exc):
    """Handle SQLAlchemy database errors."""
    logger.error(f"Database error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Database error occurred"}
    )

@app.exception_handler(500)
async def internal_server_error_handler(request, exc):
    """Handle generic internal server errors."""
    logger.error(f"Internal server error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"}
    )

# --- Add OpenAPI tags metadata ---
tags_metadata = [
    {
        "name": "Root",
        "description": "Basic API information and health checks",
    },
    {
        "name": "Dashboard", 
        "description": "Reader dashboard and reading insights",
    },
    {
        "name": "Books",
        "description": "Operations with books",
    },
    {
        "name": "Authors",
        "description": "Operations with authors", 
    },
    {
        "name": "Readers",
        "description": "Operations with readers",
    },
]

# Update app with tags metadata
app.openapi_tags = tags_metadata
# backend/app/api/__init__.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db, create_tables, seed_database
from .. import schemas, crud, models

app = FastAPI(title="STAR Library API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    create_tables()
    seed_database()

@app.get("/")
def read_root():
    return {"message": "STAR Library API"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "database": "connected"}

@app.get("/dashboard/{reader_id}", response_model=schemas.DashboardStats)
def get_dashboard_stats(reader_id: int, db: Session = Depends(get_db)):
    # Verify reader exists
    reader = crud.get_reader_by_id(db, reader_id)
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found")
    
    # Get all required data
    popular_books = crud.get_most_popular_books(db)
    popular_author = crud.get_most_popular_author(db)
    books_read_count = crud.get_reader_books_count(db, reader_id)
    top_authors = crud.get_reader_top_authors(db, reader_id)
    
    # Add computed fields to books
    for book in popular_books:
        book.readers_count = len(book.readers)
    
    # Add computed fields to popular author
    if popular_author:
        popular_author.books_count = len(popular_author.books)
        popular_author.total_readers = sum(len(book.readers) for book in popular_author.books)
    
    # Add computed fields to top authors
    for author in top_authors:
        author.books_count = len([b for b in author.books if reader in b.readers])
    
    return {
        "most_popular_books": popular_books,
        "most_popular_author": popular_author,
        "user_books_read_count": books_read_count,
        "user_top_authors": top_authors
    }

@app.get("/books/", response_model=List[schemas.Book])
def get_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    books = db.query(models.Book).offset(skip).limit(limit).all()
    for book in books:
        book.readers_count = len(book.readers)
    return books

@app.get("/authors/", response_model=List[schemas.Author])
def get_authors(db: Session = Depends(get_db)):
    authors = db.query(models.Author).all()
    for author in authors:
        author.books_count = len(author.books)
        author.total_readers = sum(len(book.readers) for book in author.books)
    return authors

@app.get("/readers/{reader_id}", response_model=schemas.Reader)
def get_reader(reader_id: int, db: Session = Depends(get_db)):
    reader = crud.get_reader_by_id(db, reader_id)
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found")
    
    reader.books_read_count = crud.get_reader_books_count(db, reader_id)
    return reader
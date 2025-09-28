# backend/app/api/__init__.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from collections import Counter

from ..database import get_db, create_tables
from .. import schemas, crud, models
from ..models import Reader, Book
from ..seed import seed_database


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
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute("SELECT 1")
        db_status = "connected"
    except SQLAlchemyError:
        db_status = "error"

    return {"status": "healthy", "database": db_status}

# Dashboard route with debug print
@app.get("/dashboard/{reader_id}", response_model=schemas.DashboardStats)
def get_dashboard(reader_id: int, db: Session = Depends(get_db)):
    reader = crud.get_reader_by_id(db, reader_id)
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found")

    most_popular_books = crud.get_most_popular_books(db)
    user_books = reader.books_read  

    author_counter = Counter(book.author for book in user_books)
    top_authors = [
        author for author, _ in author_counter.most_common(3)
    ]

    return schemas.DashboardStats(
        reader_id=reader.id,
        most_popular_books=most_popular_books,
        most_popular_author=top_authors[0] if top_authors else None,
        books_read=user_books,
        user_top_authors=top_authors
    )

@app.get("/books/", response_model=List[schemas.Book])
def get_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_books(db, skip, limit)

@app.get("/authors/", response_model=List[schemas.Author])
def get_authors(db: Session = Depends(get_db)):
    return crud.get_authors(db)

@app.get("/readers/{reader_id}", response_model=schemas.Reader)
def get_reader(reader_id: int, db: Session = Depends(get_db)):
    reader = crud.get_reader_with_stats(db, reader_id)
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found")
    return reader
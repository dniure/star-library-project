from app.api import app
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_db, create_tables, seed_database
from .models import Reader, Book
from collections import Counter



app = FastAPI(title="STAR Library API", version="1.0.0")

# Creating tables and seed data on startup
create_tables()
seed_database()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "STAR Library API is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "database": "connected"}

@app.get("/dashboard/{reader_id}")
def get_dashboard(reader_id: int, db: Session = Depends(get_db)):
    reader = db.query(Reader).filter(Reader.id == reader_id).first()
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found")

    # Example queries
    most_popular_books = db.query(Book).order_by(Book.id.desc()).limit(5).all()
    user_books = reader.books_read  # list of Book objects

    top_authors = {}
    for book in user_books:
        top_authors[book.author] = top_authors.get(book.author, 0) + 1


    author_counter = Counter(book.author.name for book in user_books)

    top_authors_list = [
        {"name": author_name, "books_count": count}
        for author_name, count in author_counter.most_common(3)
    ]


    return {
        "reader_id": reader.id,
        "most_popular_books": [
            {
                "id": b.id,
                "title": b.title,
                "description": b.description,
                "pages": b.pages,
                "genre": b.genre,
                "published_year": b.published_year,
                "readers_count": getattr(b, "readers_count", 0),
                "reading_time": getattr(b, "reading_time", 0),
                "cover_image_url": b.cover_image_url,
                "rating": getattr(b, "rating", 0),
                "author": {
                    "id": b.author.id,
                    "name": b.author.name,
                    "bio": b.author.bio,
                    "nationality": b.author.nationality
                }
            } for b in most_popular_books
        ],
        "most_popular_author": {"name": "John Doe", "total_readers": 100, "books_count": 10},
        "user_books_read_count": [
            {
                "id": b.id,
                "title": b.title,
                "description": b.description,
                "pages": b.pages,
                "cover_image_url": b.cover_image_url,
                "genre": b.genre,
                "published_year": b.published_year,
                "author": {
                    "id": b.author.id,
                    "name": b.author.name,
                    "bio": b.author.bio,
                    "nationality": b.author.nationality
                }
            } for b in user_books
        ],
        "user_top_authors": top_authors_list[:3]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

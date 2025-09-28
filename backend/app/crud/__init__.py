from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc
from typing import List, Optional
from .. import models

# --- Constants ---
DEFAULT_POPULAR_BOOKS_LIMIT = 10
DEFAULT_TOP_AUTHORS_LIMIT = 3

# --- Books ---
def get_books(db: Session, skip: int = 0, limit: int = 100) -> List[models.Book]:
    """Fetch books with readers and author info, calculate readers_count."""
    books = (
        db.query(models.Book)
        .options(joinedload(models.Book.readers), joinedload(models.Book.author))
        .offset(skip)
        .limit(limit)
        .all()
    )
    for b in books:
        b.readers_count = len(b.readers)
    return books

def get_most_popular_books(db: Session, limit: int = DEFAULT_POPULAR_BOOKS_LIMIT) -> List[models.Book]:
    """Get most read books."""
    return (
        db.query(models.Book)
        .options(joinedload(models.Book.author), joinedload(models.Book.readers))
        .outerjoin(models.Book.readers)
        .group_by(models.Book.id)
        .order_by(desc(func.count(models.Reader.id)))
        .limit(limit)
        .all()
    )


# --- Authors ---
def get_authors(db: Session) -> List[models.Author]:
    """Fetch authors with books and total readers count."""
    authors = db.query(models.Author).options(joinedload(models.Author.books).joinedload(models.Book.readers)).all()
    for author in authors:
        author.books_count = len(author.books)
        author.total_readers = sum(len(book.readers) for book in author.books)
    return authors

def get_most_popular_author(db: Session) -> Optional[models.Author]:
    """Return author with highest total readers."""
    return (
        db.query(models.Author)
        .options(joinedload(models.Author.books).joinedload(models.Book.readers))
        .outerjoin(models.Author.books)
        .outerjoin(models.Book.readers)
        .group_by(models.Author.id)
        .order_by(desc(func.count(models.Reader.id)))
        .first()
    )


# --- Readers ---
def get_reader_by_id(db: Session, reader_id: int) -> Optional[models.Reader]:
    """Fetch a reader with books and authors."""
    return (
        db.query(models.Reader)
        .options(joinedload(models.Reader.books_read).joinedload(models.Book.author))
        .filter(models.Reader.id == reader_id)
        .first()
    )

def get_reader_books_count(db: Session, reader_id: int) -> int:
    """Return total number of books read by a reader."""
    return (
        db.query(models.Book)
        .join(models.Book.readers)
        .filter(models.Reader.id == reader_id)
        .count()
    )

def get_reader_top_authors(db: Session, reader_id: int, limit: int = DEFAULT_TOP_AUTHORS_LIMIT) -> List[models.Author]:
    """Return top authors for a reader based on books read."""
    return (
        db.query(models.Author)
        .options(joinedload(models.Author.books))
        .join(models.Author.books)
        .join(models.Book.readers)
        .filter(models.Reader.id == reader_id)
        .group_by(models.Author.id)
        .order_by(desc(func.count(models.Book.id)))
        .limit(limit)
        .all()
    )

def get_reader_with_stats(db: Session, reader_id: int) -> Optional[models.Reader]:
    """Return reader with books and books_read_count."""
    reader = get_reader_by_id(db, reader_id)
    if not reader:
        return None
    reader.books_read_count = get_reader_books_count(db, reader_id)
    return reader

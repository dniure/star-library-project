"""
Data Access Layer (CRUD Operations)
Contains all database operations using SQLAlchemy ORM patterns.
"""

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc
from typing import List, Optional
from app.models import Book, Author, Reader, book_readers

# Application Constants
DEFAULT_POPULAR_BOOKS_LIMIT = 10
DEFAULT_TOP_AUTHORS_LIMIT = 3

def get_books(db: Session, skip: int = 0, limit: int = 100) -> List[Book]:
    """
    Retrieve paginated books with dynamically calculated reader counts.
    
    Args:
        db: Database session
        skip: Number of records to skip (pagination)
        limit: Maximum number of records to return
        
    Returns:
        List of Book objects with reader_count attached
    """
    books_with_counts = (
        db.query(Book, func.count(book_readers.c.reader_id).label('readers_count'))
        .options(joinedload(Book.author))
        .outerjoin(book_readers)
        .group_by(Book.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    
    # Attach computed reader counts to book objects
    return [__attach_reader_count(book, count) for book, count in books_with_counts]

def get_most_popular_books(db: Session, limit: int = DEFAULT_POPULAR_BOOKS_LIMIT) -> List[Book]:
    """
    Retrieve books ordered by reader count (most popular first).
    
    Args:
        db: Database session
        limit: Maximum number of popular books to return
        
    Returns:
        List of Book objects sorted by popularity
    """
    books_with_counts = (
        db.query(Book, func.count(book_readers.c.reader_id).label('readers_count'))
        .options(joinedload(Book.author))
        .outerjoin(book_readers)
        .group_by(Book.id)
        .order_by(func.count(book_readers.c.reader_id).desc())
        .limit(limit)
        .all()
    )
    
    return [__attach_reader_count(book, count) for book, count in books_with_counts]

def get_authors(db: Session) -> List[Author]:
    """
    Retrieve all authors with computed book counts and reader statistics.
    
    Returns:
        List of Author objects with books_count and total_readers attached
    """
    authors = db.query(Author).options(joinedload(Author.books)).all()
    
    for author in authors:
        author.books_count = len(author.books)
        author.total_readers = sum(len(book.readers) for book in author.books)
    
    return authors

def get_most_popular_author(db: Session) -> Optional[Author]:
    """
    Identify author with the highest total readership across all their books.
    
    Returns:
        Author object with highest reader count, or None if no authors exist
    """
    authors = get_authors(db)
    return max(authors, key=lambda author: author.total_readers) if authors else None

def get_reader(db: Session, reader_id: int) -> Optional[Reader]:
    """
    Retrieve reader by ID with their reading history and book authors.
    
    Args:
        reader_id: Unique identifier for the reader
        
    Returns:
        Reader object with books_read and author relationships loaded
    """
    return (
        db.query(Reader)
        .options(joinedload(Reader.books_read).joinedload(Book.author))
        .filter(Reader.id == reader_id)
        .first()
    )

def get_reader_top_authors(db: Session, reader_id: int, limit: int = DEFAULT_TOP_AUTHORS_LIMIT) -> List[Author]:
    """
    Calculate top authors for a reader based on books read count.
    
    Args:
        reader_id: Reader to analyze
        limit: Maximum number of top authors to return
        
    Returns:
        List of Author objects sorted by books read count
    """
    reader = get_reader(db, reader_id)
    if not reader or not reader.books_read:
        return []
    
    # Count books per author
    author_counts = {}
    for book in reader.books_read:
        if book.author:
            author_id = book.author.id
            author_counts.setdefault(author_id, {'author': book.author, 'count': 0})
            author_counts[author_id]['count'] += 1
    
    # Sort by count and return top authors
    sorted_authors = sorted(author_counts.values(), key=lambda x: x['count'], reverse=True)
    return [item['author'] for item in sorted_authors[:limit]]

def get_reader_with_stats(db: Session, reader_id: int) -> Optional[Reader]:
    """
    Retrieve reader with additional computed statistics.
    
    Returns:
        Reader object with books_read_count attribute added
    """
    reader = get_reader(db, reader_id)
    if reader:
        reader.books_read_count = len(reader.books_read)
    return reader

def __attach_reader_count(book: Book, readers_count: int) -> Book:
    """Helper function to attach reader count to book object."""
    book.readers_count = readers_count
    return book
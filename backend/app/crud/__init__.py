"""
crud.py
-------------------
Contains all Create, Read, Update, Delete (CRUD) functions.
These functions interact directly with SQLAlchemy Models and the database session.
"""

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc
from typing import List, Optional
from .. import models

# Constants
DEFAULT_POPULAR_BOOKS_LIMIT = 10
DEFAULT_TOP_AUTHORS_LIMIT = 3

# Books CRUD Operations

def get_books(db: Session, skip: int = 0, limit: int = 100) -> List[models.Book]:
    """Fetch books with author info and calculate readers_count in SQL."""
    
    books_data = (
        db.query(
            models.Book,
            func.count(models.Reader.id).label('readers_count')
        )
        .options(joinedload(models.Book.author)) # Still eager load the Author object
        .outerjoin(models.Book.readers)
        .group_by(models.Book.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    
    # Process results: Unpack the tuple and assign the calculated count
    books = []
    for book_model, readers_count in books_data:
        book_model.readers_count = readers_count
        books.append(book_model)
        
    return books

def get_most_popular_books(db: Session, limit: int = DEFAULT_POPULAR_BOOKS_LIMIT) -> List[models.Book]:
    """Get most read books based on the count of unique readers."""
    return (
        db.query(models.Book)
        .options(joinedload(models.Book.author), joinedload(models.Book.readers))
        # Outer join ensures books with zero readers are included
        .outerjoin(models.Book.readers)
        .group_by(models.Book.id)
        # Order by the count of reader IDs in descending order
        .order_by(desc(func.count(models.Reader.id)))
        .limit(limit)
        .all()
    )

# Authors CRUD Operations
def get_authors(db: Session) -> List[models.Author]:
    """Fetch authors with their total books and total readers count using SQL aggregation."""
    
    # Define a subquery for total readers (requires a few joins)
    # The count will be associated with the Author object later.
    total_readers_count = func.count(models.Reader.id).label('total_readers')

    authors_data = (
        db.query(
            models.Author,
            func.count(models.Book.id).label('books_count'),
            total_readers_count
        )
        # Outer joins ensure authors with no books/readers are included
        .outerjoin(models.Author.books)
        .outerjoin(models.Book.readers)
        .group_by(models.Author.id)
        .all()
    )
    
    # Process results: The query returns tuples, map the counts back to the Author object.
    authors = []
    for author_model, books_count, total_readers in authors_data:
        # Attach virtual fields to the Author model object
        author_model.books_count = books_count
        author_model.total_readers = total_readers
        authors.append(author_model)

    return authors

def get_most_popular_author(db: Session) -> Optional[models.Author]:
    """Return author with highest total readers across all their books."""
    return (
        db.query(models.Author)
        # Eagerly load nested relationships (books -> readers)
        .options(joinedload(models.Author.books).joinedload(models.Book.readers))
        .outerjoin(models.Author.books)
        .outerjoin(models.Book.readers)
        .group_by(models.Author.id)
        .order_by(desc(func.count(models.Reader.id)))
        .first()
    )

# Readers CRUD Operations
def get_reader_by_id(db: Session, reader_id: int) -> Optional[models.Reader]:
    """Fetch a reader with their books read and the author details for those books."""
    return (
        db.query(models.Reader)
        # Eagerly load books_read, and for each book, load its author
        .options(joinedload(models.Reader.books_read).joinedload(models.Book.author))
        .filter(models.Reader.id == reader_id)
        .first()
    )

def get_reader_top_authors(db: Session, reader_id: int, limit: int = DEFAULT_TOP_AUTHORS_LIMIT) -> List[models.Author]:
    """Return top authors for a reader based on how many of their books the reader has read."""
    return (
        db.query(models.Author)
        .options(joinedload(models.Author.books))
        .join(models.Author.books)
        .join(models.Book.readers)
        .filter(models.Reader.id == reader_id)
        # Group by author to count books per author read by this specific reader
        .group_by(models.Author.id)
        .order_by(desc(func.count(models.Book.id)))
        .limit(limit)
        .all()
    )

def get_reader_with_stats(db: Session, reader_id: int) -> Optional[models.Reader]:
    """Return reader object and attach calculated stats (books_read_count)."""
    
    # get_reader_by_id already eagerly loads all books_read.
    reader = get_reader_by_id(db, reader_id)
    
    if not reader:
        return None
    
    # Calculate the count from the eagerly loaded list..
    reader.books_read_count = len(reader.books_read)
    return reader
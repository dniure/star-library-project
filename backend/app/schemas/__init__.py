"""
API Schemas (Pydantic Models)
Defines request/response contracts and data validation rules.
"""

from pydantic import BaseModel
from typing import List, Optional

class AuthorBase(BaseModel):
    """Base author schema with core biographical fields."""
    name: str
    bio: Optional[str] = None
    nationality: Optional[str] = None

    model_config = {"from_attributes": True}

class AuthorCreate(AuthorBase):
    """Schema for creating new authors (matches base for now)."""
    pass

class Author(AuthorBase):
    """Complete author schema with database ID and computed statistics."""
    id: int
    books_count: Optional[int] = 0  # Computed: total books by this author
    total_readers: Optional[int] = 0  # Computed: total readers across all books

class BookBase(BaseModel):
    """Base book schema with essential metadata."""
    title: str
    description: Optional[str] = None
    pages: int
    genre: str
    published_year: int

class BookCreate(BookBase):
    """Schema for creating new books (requires author reference)."""
    author_id: int

class Book(BookBase):
    """Complete book schema with relationships and computed fields."""
    id: int
    readers_count: Optional[int] = 0  # Computed: number of readers
    reading_time: Optional[int] = 0  # Estimated reading duration
    cover_image_url: Optional[str] = None
    rating: Optional[float] = 0.0
    author: Author  # Nested author information

    model_config = {"from_attributes": True}

class ReaderBase(BaseModel):
    """Base reader schema with profile information."""
    name: str
    email: str
    favorite_genre: Optional[str] = None

class ReaderCreate(ReaderBase):
    """Schema for creating new readers."""
    pass

class Reader(ReaderBase):
    """Complete reader schema with reading history."""
    id: int
    books_read: List[Book] = []  # Reader's personal library

class DashboardData(BaseModel):
    """Comprehensive data schema for reader dashboard."""
    reader_id: int
    reader_name: str
    most_popular_books: List[Book]  # Community trending books
    most_popular_author: Optional[Author] = None  # Top author by readership
    user_books_read: List[Book]  # Reader's personal reading history
    user_top_authors: List[Author]  # Reader's most-read authors

    model_config = {"from_attributes": True}
"""
schemas.py
-------------------
Defines all Pydantic schemas (data transfer objects) for API input validation
and output serialization (response models).
"""

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


# Author Schemas
class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] = None
    nationality: Optional[str] = None

    model_config = {"from_attributes": True}


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    books_count: Optional[int] = 0       # Computed field
    total_readers: Optional[int] = 0     # Computed field

    model_config = {"from_attributes": True}


# Book Schemas
class BookBase(BaseModel):
    title: str
    description: Optional[str] = None
    pages: int
    genre: str
    published_year: int


class BookCreate(BookBase):
    author_id: int


class Book(BookBase):
    id: int
    readers_count: Optional[int] = 0     # Computed field
    reading_time: Optional[int] = 0
    cover_image_url: Optional[str] = None
    rating: Optional[float] = 0.0
    author: Author                       # Nested Author schema

    model_config = {"from_attributes": True}


# Reader Schemas
class ReaderBase(BaseModel):
    name: str
    email: str
    favorite_genre: Optional[str] = None


class ReaderCreate(ReaderBase):
    pass


class Reader(ReaderBase):
    id: int
    join_date: datetime
    books_read_count: Optional[int] = 0  # Computed field
    books_read: Optional[List[Book]] = [] # Nested list of Book schemas

    model_config = {"from_attributes": True}


# Dashboard Schema (Complex aggregation of data for a single endpoint)
class DashboardStats(BaseModel):
    reader_id: int
    most_popular_books: List[Book]
    most_popular_author: Optional[Author] = None
    books_read: List[Book]
    reader_top_authors: List[Author]

    model_config = {"from_attributes": True}
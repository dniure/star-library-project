# backend/app/schemas/__init__.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# ------------------------
# Author Schemas
# ------------------------
class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] = None
    nationality: Optional[str] = None

    model_config = {"from_attributes": True}

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    id: int
    books_count: Optional[int] = None   # computed dynamically
    total_readers: Optional[int] = None # computed dynamically

    model_config = {"from_attributes": True}


# ------------------------
# Book Schemas
# ------------------------
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
    readers_count: Optional[int] = 0
    reading_time: Optional[int] = 0
    cover_image_url: Optional[str] = None
    rating: Optional[float] = 0.0
    author: Author

    model_config = {"from_attributes": True}

# ------------------------
# Reader Schemas
# ------------------------
class ReaderBase(BaseModel):
    name: str
    email: str
    favorite_genre: Optional[str] = None

class ReaderCreate(ReaderBase):
    pass

class Reader(ReaderBase):
    id: int
    join_date: datetime
    books_read_count: Optional[int] = None  # computed dynamically
    books_read: Optional[List[Book]] = []   # relationship: books the reader read

    model_config = {"from_attributes": True}


# ------------------------
# Dashboard Schema
# ------------------------
class DashboardStats(BaseModel):
    reader_id: int
    most_popular_books: List[Book]
    most_popular_author: Author
    books_read: List[Book]
    user_top_authors: List[Author]

    model_config = {"from_attributes": True}

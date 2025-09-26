# backend/app/schemas/__init__.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] = None
    nationality: Optional[str] = None

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    id: int
    books_count: Optional[int] = None
    total_readers: Optional[int] = None
    
    class Config:
        orm_mode = True

class BookBase(BaseModel):
    title: str
    description: Optional[str] = None
    genre: Optional[str] = None
    pages: Optional[int] = None
    published_year: Optional[int] = None

class BookCreate(BookBase):
    author_id: int

class Book(BookBase):
    id: int
    author: Author
    readers_count: Optional[int] = None
    
    class Config:
        orm_mode = True

class ReaderBase(BaseModel):
    name: str
    email: str
    favorite_genre: Optional[str] = None

class ReaderCreate(ReaderBase):
    pass

class Reader(ReaderBase):
    id: int
    join_date: datetime
    books_read_count: Optional[int] = None
    
    class Config:
        orm_mode = True

class DashboardStats(BaseModel):
    most_popular_books: List[Book]
    most_popular_author: Author
    user_books_read_count: int
    user_top_authors: List[Author]
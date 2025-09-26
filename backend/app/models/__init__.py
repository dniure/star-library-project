# backend/app/models/__init__.py

from .base import Base
from .author import Author
from .book import Book, book_readers
from .reader import Reader
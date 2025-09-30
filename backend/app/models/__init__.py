"""
Database Models (SQLAlchemy ORM)
Defines database schema and relationships between entities.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

# Association table for many-to-many relationship between books and readers
book_readers = Table(
    "book_readers",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("books.id"), primary_key=True),
    Column("reader_id", Integer, ForeignKey("readers.id"), primary_key=True),
    Column("read_at", DateTime, default=datetime.utcnow),  # Track reading timestamps
)

class Author(Base):
    """Author entity representing book writers with biographical information."""
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    bio = Column(String)  # Author biography
    birth_date = Column(String)  # Could be Date type in production
    nationality = Column(String)

    # Relationship: Author has many Books
    books = relationship("Book", back_populates="author")

class Book(Base):
    """Book entity representing published works with metadata."""
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String)  # Book synopsis
    genre = Column(String)  # Fiction, Fantasy, Mystery, etc.
    pages = Column(Integer)
    published_year = Column(Integer)
    cover_image_url = Column(String)  # URL to book cover image
    reading_time = Column(Integer, default=0)  # Estimated reading time in hours
    rating = Column(Integer, default=4)  # Average user rating
    
    # Foreign key relationship to Author
    author_id = Column(Integer, ForeignKey("authors.id"))
    
    # Relationships
    author = relationship("Author", back_populates="books")
    readers = relationship("Reader", secondary=book_readers, back_populates="books_read")

class Reader(Base):
    """Reader entity representing library users with reading preferences."""
    __tablename__ = "readers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    join_date = Column(DateTime, default=datetime.utcnow)
    favorite_genre = Column(String)

    # Many-to-many relationship with Books through book_readers
    books_read = relationship("Book", secondary=book_readers, back_populates="readers")
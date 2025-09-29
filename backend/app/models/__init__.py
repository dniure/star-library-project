"""
models.py
-------------------
Defines the SQL database schema using SQLAlchemy ORM.
All classes inherit from Base and map directly to database tables.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime, timezone

Base = declarative_base()

# Many-to-Many Association Table
book_readers = Table(
    "book_readers",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("books.id")),
    Column("reader_id", Integer, ForeignKey("readers.id")),
    Column("read_at", DateTime, default=lambda: datetime.now(timezone.utc)),
)


# Author Model (One-to-Many relationship with Books)
class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    bio = Column(String)
    birth_date = Column(String)
    nationality = Column(String)

    # Relationship to books (list of Book objects)
    books = relationship("Book", back_populates="author")


# Book Model (Many-to-One with Author, Many-to-Many with Reader)
class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String)
    genre = Column(String)
    pages = Column(Integer)
    published_year = Column(Integer)
    cover_image_url = Column(String)

    # Temporary/Calculated fields for ORM use
    readers_count = Column(Integer, default=0)
    reading_time = Column(Integer, default=0)
    rating = Column(Integer, default=4)

    # Foreign Key to Author
    author_id = Column(Integer, ForeignKey("authors.id"))
    author = relationship("Author", back_populates="books")
    
    # Many-to-Many relationship to Reader via book_readers table
    readers = relationship("Reader", secondary=book_readers, back_populates="books_read")


# Reader Model (Many-to-Many relationship with Book)
class Reader(Base):
    __tablename__ = "readers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    join_date = Column(DateTime, default=datetime.utcnow)
    favorite_genre = Column(String)

    # Many-to-Many relationship to Book via book_readers table
    books_read = relationship("Book", secondary=book_readers, back_populates="readers")
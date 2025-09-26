from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

# Many-to-many table
book_readers = Table(
    "book_readers",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("books.id")),
    Column("reader_id", Integer, ForeignKey("readers.id")),
    Column("read_at", DateTime, default=datetime.utcnow),
)

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String)
    genre = Column(String)
    pages = Column(Integer)
    published_year = Column(Integer)
    cover_image_url = Column(String)

    author_id = Column(Integer, ForeignKey("authors.id"))
    author = relationship("Author", back_populates="books")
    readers = relationship("Reader", secondary=book_readers, back_populates="books_read")

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base
from .book import book_readers

class Reader(Base):
    __tablename__ = "readers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    join_date = Column(DateTime, default=datetime.utcnow)
    favorite_genre = Column(String)

    books_read = relationship("Book", secondary=book_readers, back_populates="readers")

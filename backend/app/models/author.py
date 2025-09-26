from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    bio = Column(String)
    birth_date = Column(String)
    nationality = Column(String)

    books = relationship("Book", back_populates="author")
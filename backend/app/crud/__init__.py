# backend/app/crud/__init__.py
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List
from .. import models

def get_most_popular_books(db: Session, limit: int = 10) -> List[models.Book]:
    return db.query(models.Book)\
        .outerjoin(models.Book.readers)\
        .group_by(models.Book.id)\
        .order_by(desc(func.count(models.Reader.id)))\
        .limit(limit)\
        .all()

def get_most_popular_author(db: Session) -> models.Author:
    author = db.query(models.Author)\
        .outerjoin(models.Author.books)\
        .outerjoin(models.Book.readers)\
        .group_by(models.Author.id)\
        .order_by(desc(func.count(models.Reader.id)))\
        .first()
    return author

def get_reader_books_count(db: Session, reader_id: int) -> int:
    return db.query(models.Book)\
        .join(models.Book.readers)\
        .filter(models.Reader.id == reader_id)\
        .count()

def get_reader_top_authors(db: Session, reader_id: int, limit: int = 3) -> List[models.Author]:
    return db.query(models.Author)\
        .join(models.Author.books)\
        .join(models.Book.readers)\
        .filter(models.Reader.id == reader_id)\
        .group_by(models.Author.id)\
        .order_by(desc(func.count(models.Book.id)))\
        .limit(limit)\
        .all()

def get_reader_by_id(db: Session, reader_id: int) -> models.Reader:
    return db.query(models.Reader).filter(models.Reader.id == reader_id).first()
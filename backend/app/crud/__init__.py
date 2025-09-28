# backend/app/crud/__init__.py
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc
from typing import List
from .. import models

def get_most_popular_books(db: Session, limit: int = 10) -> List[models.Book]:
    return (
        db.query(models.Book)
        .options(joinedload(models.Book.author), joinedload(models.Book.readers))  # eager load relationships
        .outerjoin(models.Book.readers)
        .group_by(models.Book.id)
        .order_by(desc(func.count(models.Reader.id)))
        .limit(limit)
        .all()
    )

def get_most_popular_author(db: Session) -> models.Author:
    return (
        db.query(models.Author)
        .options(joinedload(models.Author.books).joinedload(models.Book.readers))  # eager load nested books + readers
        .outerjoin(models.Author.books)
        .outerjoin(models.Book.readers)
        .group_by(models.Author.id)
        .order_by(desc(func.count(models.Reader.id)))
        .first()
    )

def get_reader_books_count(db: Session, reader_id: int) -> int:
    return (
        db.query(models.Book)
        .join(models.Book.readers)
        .filter(models.Reader.id == reader_id)
        .count()
    )

def get_reader_top_authors(db: Session, reader_id: int, limit: int = 3) -> List[models.Author]:
    return (
        db.query(models.Author)
        .options(joinedload(models.Author.books))  # eager load books
        .join(models.Author.books)
        .join(models.Book.readers)
        .filter(models.Reader.id == reader_id)
        .group_by(models.Author.id)
        .order_by(desc(func.count(models.Book.id)))
        .limit(limit)
        .all()
    )

def get_reader_by_id(db: Session, reader_id: int) -> models.Reader:
    return (
        db.query(models.Reader)
        .options(joinedload(models.Reader.books_read).joinedload(models.Book.author))  # eager load books + author
        .filter(models.Reader.id == reader_id)
        .first()
    )

def get_books(db: Session, skip=0, limit=100) -> List[models.Book]:
    books = (
        db.query(models.Book)
        .options(joinedload(models.Book.readers), joinedload(models.Book.author))  # eager load readers + author
        .offset(skip)
        .limit(limit)
        .all()
    )
    for b in books:
        b.readers_count = len(b.readers)  # safe now, no N+1
    return books

def get_authors(db: Session) -> List[models.Author]:
    authors = (
        db.query(models.Author)
        .options(joinedload(models.Author.books).joinedload(models.Book.readers))  # eager load books + readers
        .all()
    )
    for author in authors:
        author.books_count = len(author.books)
        author.total_readers = sum(len(book.readers) for book in author.books)
    return authors

def get_reader_with_stats(db: Session, reader_id: int) -> models.Reader:
    reader = (
        db.query(models.Reader)
        .options(joinedload(models.Reader.books_read).joinedload(models.Book.author))  # eager load books + authors
        .filter(models.Reader.id == reader_id)
        .first()
    )
    if not reader:
        return None
    reader.books_read_count = get_reader_books_count(db, reader_id)
    return reader

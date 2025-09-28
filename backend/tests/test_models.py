# backend/tests/test_models.py

from app import models
from sqlalchemy import inspect

def test_author_book_relationship(db):
    author = db.query(models.Author).filter(models.Author.id == 1).first()
    assert author is not None
    assert len(author.books) > 0
    assert author.books[0].title == "HP and the Sorcerer's Stone"

def test_book_reader_relationship(db):
    book = db.query(models.Book).filter(models.Book.id == 1).first()
    assert book is not None
    assert len(book.readers) > 0
    assert book.readers[0].name == "Alice"

def test_reader_books(db):
    reader = db.query(models.Reader).filter(models.Reader.id == 1).first()
    assert reader is not None
    assert len(reader.books_read) > 0
    assert reader.books_read[0].title == "HP and the Sorcerer's Stone"

def test_create_tables(db):
    """Test that tables are properly created and relationships work"""
    # Test that we can query the seeded data (this proves tables exist)
    authors = db.query(models.Author).all()
    assert len(authors) == 2
    assert authors[0].name == "J.K. Rowling"
    
    books = db.query(models.Book).all() 
    assert len(books) == 2
    assert books[0].title == "HP and the Sorcerer's Stone"
    
    readers = db.query(models.Reader).all()
    assert len(readers) == 2
    assert readers[0].name == "Alice"
    
    # Test relationships work (this proves foreign keys and associations work)
    reader1 = db.query(models.Reader).filter(models.Reader.id == 1).first()
    assert len(reader1.books_read) == 1
    assert reader1.books_read[0].title == "HP and the Sorcerer's Stone"
# backend/tests/test_crud.py

from app import crud, models

def test_get_most_popular_books(db):
    books = crud.get_most_popular_books(db)
    assert len(books) > 0
    # Book 1 should be more popular (has 1 reader) than book 2 (has 0 readers)
    assert books[0].id == 1
    assert books[0].readers_count >= 0

def test_get_most_popular_author(db):
    author = crud.get_most_popular_author(db)
    assert author is not None
    assert hasattr(author, "books")
    # J.K. Rowling should be more popular (has book with reader)
    assert author.name == "J.K. Rowling"

def test_get_reader_top_authors(db):
    top_authors = crud.get_reader_top_authors(db, reader_id=1)
    assert len(top_authors) > 0
    assert all(isinstance(a, models.Author) for a in top_authors)
    # Reader 1 has read books by J.K. Rowling
    assert top_authors[0].name == "J.K. Rowling"

def test_get_books(db):
    books = crud.get_books(db)
    assert len(books) == 2
    assert all(hasattr(b, "readers_count") for b in books)
    assert books[0].title == "HP and the Sorcerer's Stone"
    assert books[1].title == "1984"

def test_get_authors(db):
    authors = crud.get_authors(db)
    assert len(authors) == 2
    assert all(hasattr(a, "total_readers") for a in authors)
    assert all(hasattr(a, "books_count") for a in authors)

def test_get_reader_with_stats(db):
    reader = crud.get_reader_with_stats(db, reader_id=1)
    assert reader is not None
    assert reader.books_read_count == 1  # Reader 1 has read 1 book
    assert reader.name == "Alice"
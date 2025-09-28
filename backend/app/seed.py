## seed.py

from sqlalchemy import insert
from .database import SessionLocal
from .models import Author, Book, Reader
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def seed_database():
    db = SessionLocal()
    try:
        if db.query(Author).count() > 0:
            logger.info("Database already seeded. Skipping...")
            return

        logger.info("Database already seeded. Skipping...")

        # --- Authors ---
        authors = [
            Author(name="J.K. Rowling", bio="British author best known for Harry Potter", nationality="British"),
            Author(name="Brandon Sanderson", bio="American fantasy and science fiction writer", nationality="American"),
            Author(name="Stephen King", bio="American author of horror, supernatural fiction", nationality="American"),
            Author(name="Agatha Christie", bio="English writer known for detective novels", nationality="British"),
        ]
        db.bulk_save_objects(authors)
        db.flush()

        # --- Books ---
        books = [
            Book(
                title="Harry Potter and the Philosopher's Stone",
                genre="Fantasy",
                pages=223,
                author_id=authors[0].id,
                published_year=1997,
                readers_count=1200,
                reading_time=7,
                description="Harry discovers he is a wizard and attends Hogwarts School of Witchcraft and Wizardry, beginning a journey full of magic, friendship, and danger."
            ),
            Book(
                title="Harry Potter and the Chamber of Secrets",
                genre="Fantasy",
                pages=251,
                author_id=authors[0].id,
                published_year=1998,
                readers_count=1150,
                reading_time=8,
                description="Harry returns to Hogwarts and must uncover the mystery behind a hidden chamber threatening the students with petrification."
            ),
            # ... (keep the rest of your book objects here unchanged)
        ]
        db.bulk_save_objects(books)
        db.flush()

        # --- Readers ---
        readers = [
            Reader(name="James Bernhardt", email="james.bernhardt@subtera.tech", favorite_genre="Sci-Fi"),
            Reader(name="Michael Chen", email="michael@email.com", favorite_genre="Mystery"),
            Reader(name="Sarah Williams", email="sarah@email.com", favorite_genre="Horror"),
            Reader(name="David Brown", email="david@email.com", favorite_genre="Fantasy"),
            Reader(name="Lisa Garcia", email="lisa@email.com", favorite_genre="Mystery"),
        ]
        db.bulk_save_objects(readers)
        db.flush()

        # --- Book-Reader Relationships ---
        reading_relationships = []
        for book in books[:8]:
            reading_relationships.append({"book_id": book.id, "reader_id": readers[0].id})
        for book in books[12:15]:
            reading_relationships.append({"book_id": book.id, "reader_id": readers[1].id})
        for book in books[8:12]:
            reading_relationships.append({"book_id": book.id, "reader_id": readers[2].id})
        for idx in [0, 4, 9]:
            reading_relationships.append({"book_id": books[idx].id, "reader_id": readers[3].id})
        for book in books[12:15]:
            reading_relationships.append({"book_id": book.id, "reader_id": readers[4].id})

        db.execute(insert(book_readers), reading_relationships)
        db.commit()

        logger.info("Database seeded successfully with realistic data!")

    except Exception as e:
        db.rollback()
        logger.error(f"Error seeding database: {e}", exc_info=True)
        raise
    finally:
        db.close()

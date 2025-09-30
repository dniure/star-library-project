"""
seed.py
-------------------
Standalone utility function to populate the database with initial, test data.
Manually manages session lifecycle (create/commit/close).
"""

from sqlalchemy import insert
from .database import SessionLocal
from .models import Book, Author, Reader, book_readers
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def seed_database():
    """Seed the database with initial authors, books, readers, and relationships."""
    db = SessionLocal()
    try:
        # Check if any Author exists to prevent re-seeding
        if db.query(Author).count() > 0:
            logger.info("Database already seeded. Skipping...")
            return

        # Authors
        authors = [
            Author(name="J.K. Rowling", bio="British author best known for Harry Potter", nationality="British"),
            Author(name="Brandon Sanderson", bio="American fantasy and science fiction writer", nationality="American"),
            Author(name="Stephen King", bio="American author of horror, supernatural fiction", nationality="American"),
            Author(name="Agatha Christie", bio="English writer known for detective novels", nationality="British"),
        ]
        db.bulk_save_objects(authors)
        db.flush() # Flush to get generated Author IDs

        # Books
        books = [
            
            # Rowling (index 0)
            Book(title="Harry Potter and the Philosopher's Stone", genre="Fantasy", pages=223, author_id=authors[0].id, published_year=1997, readers_count=1200, reading_time=7, description="Harry discovers he is a wizard..."),
            Book(title="Harry Potter and the Chamber of Secrets", genre="Fantasy", pages=251, author_id=authors[0].id, published_year=1998, readers_count=950, reading_time=8, description="The second year at Hogwarts..."),
            Book(title="Harry Potter and the Prisoner of Azkaban", genre="Fantasy", pages=317, author_id=authors[0].id, published_year=1999, readers_count=1100, reading_time=10, description="Sirius Black escapes Azkaban..."),
            
            # Sanderson (index 1)
            Book(title="The Way of Kings", genre="Epic Fantasy", pages=1007, author_id=authors[1].id, published_year=2010, readers_count=800, reading_time=35, description="First book in The Stormlight Archive..."),
            Book(title="Mistborn: The Final Empire", genre="Fantasy", pages=544, author_id=authors[1].id, published_year=2006, readers_count=1500, reading_time=18, description="A world blanketed in ash..."),
            Book(title="Elantris", genre="Fantasy", pages=638, author_id=authors[1].id, published_year=2005, readers_count=400, reading_time=22, description="The city of Elantris falls..."),
            Book(title="Warbreaker", genre="Fantasy", pages=688, author_id=authors[1].id, published_year=2009, readers_count=350, reading_time=24, description="Two sisters become pawns..."),
            
            # King (index 2)
            Book(title="It", genre="Horror", pages=1138, author_id=authors[2].id, published_year=1986, readers_count=2000, reading_time=40, description="Seven children confront an ancient evil..."),
            Book(title="The Shining", genre="Horror", pages=447, author_id=authors[2].id, published_year=1977, readers_count=1800, reading_time=15, description="A family spends winter at the Overlook Hotel..."),
            Book(title="Carrie", genre="Horror", pages=199, author_id=authors[2].id, published_year=1974, readers_count=900, reading_time=6, description="A shy girl with telekinetic powers..."),
            Book(title="The Stand", genre="Post-Apocalyptic", pages=823, author_id=authors[2].id, published_year=1978, readers_count=1300, reading_time=28, description="A superflu pandemic wipes out humanity..."),

            # Christie (index 3)
            Book(title="And Then There Were None", genre="Mystery", pages=272, author_id=authors[3].id, published_year=1939, readers_count=2500, reading_time=9, description="Ten strangers trapped on an island..."),
            Book(title="Murder on the Orient Express", genre="Mystery", pages=256, author_id=authors[3].id, published_year=1934, readers_count=2100, reading_time=8, description="Hercule Poirot investigates a murder on a train..."),
            Book(title="The A.B.C. Murders", genre="Mystery", pages=288, author_id=authors[3].id, published_year=1936, readers_count=1000, reading_time=9, description="A killer working through the alphabet..."),
            Book(title="The Murder of Roger Ackroyd", genre="Mystery", pages=288, author_id=authors[3].id, published_year=1926, readers_count=900, reading_time=9, description="A case with a shocking twist..."),
        ]
        db.bulk_save_objects(books)
        db.flush() # Flush to get generated Book IDs

        # Readers (Users)
        readers = [
            Reader(name="James Bernhardt", email="james.b@subtera.tech", favorite_genre="Mystery"),
            Reader(name="Michael Chen", email="michael@example.com", favorite_genre="Fantacy"),
            Reader(name="Sarah Williams", email="sarah@example.com", favorite_genre="Horror"),
            Reader(name="David Brown", email="david@example.com", favorite_genre="Epic Fantasy"),
            Reader(name="Lisa Garcia", email="lisa@example.com", favorite_genre="Mystery"),
        ]
        db.bulk_save_objects(readers)
        db.flush()

        # Relationships: Define the many-to-many associations (who read what)
        relationships = []

        # Reader 1
        for i in [0, 1, 2, 4, 9]:
            relationships.append({"book_id": books[i].id, "reader_id": readers[0].id})
        
        # Reader 2
        for i in range(11, 15):
            relationships.append({"book_id": books[i].id, "reader_id": readers[1].id})

        # Reader 3
        for i in range(7, 11):
            relationships.append({"book_id": books[i].id, "reader_id": readers[2].id})
        relationships.append({"book_id": books[1].id, "reader_id": readers[2].id})

        # Reader 4
        for i in [3, 5, 6]:
            relationships.append({"book_id": books[i].id, "reader_id": readers[3].id})
        
        # Reader 5
        for i in [7, 11, 12]:
            relationships.append({"book_id": books[i].id, "reader_id": readers[4].id})


        db.execute(insert(book_readers), relationships)
        db.commit()

        logger.info("Database seeded successfully!")

    except Exception as e:
        db.rollback()
        logger.error(f"Error seeding database: {e}", exc_info=True)
        raise
    finally:
        # Close the manually created session
        db.close()
"""
Database Seeding Utility
Populates database with initial test data for development and demonstration.
"""

from sqlalchemy import insert
from .database import SessionLocal
from .models import Book, Author, Reader, book_readers
import logging

logger = logging.getLogger(__name__)

def seed_database():
    """
    Populate database with sample authors, books, readers, and reading relationships.
    Clears existing data to ensure clean state on each application start.
    """
    db = SessionLocal()
    try:
        __clear_existing_data(db)
        authors = __create_authors(db)
        books = __create_books(db, authors)
        readers = __create_readers(db)
        __create_reading_relationships(db, books, readers)
        
        logger.info("Database seeded successfully with sample data")
        
    except Exception as e:
        db.rollback()
        logger.error(f"Seeding failed: {e}")
        raise
    finally:
        db.close()

def __clear_existing_data(db):
    """Remove existing data to start with clean database."""
    logger.info("Clearing existing database...")
    # Clear in dependency order to respect foreign key constraints
    db.execute(book_readers.delete())
    db.execute(Book.__table__.delete())
    db.execute(Author.__table__.delete())
    db.execute(Reader.__table__.delete())
    db.commit()

def __create_authors(db):
    """Create sample authors with biographical information."""
    authors = [
        Author(
            name="J.K. Rowling",
            bio="British author best known for the Harry Potter series",
            nationality="British"
        ),
        Author(
            name="Brandon Sanderson", 
            bio="American fantasy and science fiction writer",
            nationality="American"
        ),
        Author(
            name="Stephen King",
            bio="Master of horror and supernatural fiction",
            nationality="American"
        ),
        Author(
            name="Agatha Christie",
            bio="Queen of mystery and detective novels", 
            nationality="British"
        ),
    ]
    db.add_all(authors)
    db.commit()
    logger.info(f"Created {len(authors)} authors")
    return authors

def __create_books(db, authors):
    """Create sample books across various genres and authors."""
    books = [
        # J.K. Rowling - Fantasy
        Book(title="Harry Potter and the Philosopher's Stone", genre="Fantasy", 
             pages=223, author_id=authors[0].id, published_year=1997, reading_time=7,
             description="A young wizard discovers his magical heritage..."),
        Book(title="Harry Potter and the Chamber of Secrets", genre="Fantasy",
             pages=251, author_id=authors[0].id, published_year=1998, reading_time=8,
             description="Harry's second year brings new magical dangers..."),
        Book(title="Harry Potter and the Prisoner of Azkaban", genre="Fantasy",
             pages=317, author_id=authors[0].id, published_year=1999, reading_time=10,
             description="A dangerous prisoner escapes magical prison..."),
        
        # Brandon Sanderson - Epic Fantasy
        Book(title="The Way of Kings", genre="Epic Fantasy",
             pages=1007, author_id=authors[1].id, published_year=2010, reading_time=35,
             description="First volume in the acclaimed Stormlight Archive..."),
        Book(title="Mistborn: The Final Empire", genre="Fantasy",
             pages=544, author_id=authors[1].id, published_year=2006, reading_time=18,
             description="A crew of thieves plots to overthrow a god..."),
        Book(title="Elantris", genre="Fantasy", 
             pages=638, author_id=authors[1].id, published_year=2005, reading_time=22,
             description="A fallen city and its cursed inhabitants..."),
        Book(title="Warbreaker", genre="Fantasy",
             pages=688, author_id=authors[1].id, published_year=2009, reading_time=24,
             description="Magic system based on colors and breath..."),
        
        # Stephen King - Horror
        Book(title="It", genre="Horror",
             pages=1138, author_id=authors[2].id, published_year=1986, reading_time=40,
             description="Childhood friends confront a shape-shifting evil..."),
        Book(title="The Shining", genre="Horror", 
             pages=447, author_id=authors[2].id, published_year=1977, reading_time=15,
             description="A family's winter in a haunted hotel..."),
        Book(title="Carrie", genre="Horror",
             pages=199, author_id=authors[2].id, published_year=1974, reading_time=6,
             description="A bullied teen with telekinetic powers seeks revenge..."),
        Book(title="The Stand", genre="Post-Apocalyptic",
             pages=823, author_id=authors[2].id, published_year=1978, reading_time=28,
             description="Survivors of a pandemic choose sides in epic battle..."),
        
        # Agatha Christie - Mystery
        Book(title="And Then There Were None", genre="Mystery",
             pages=272, author_id=authors[3].id, published_year=1939, reading_time=9,
             description="Ten strangers murdered one by one on isolated island..."),
        Book(title="Murder on the Orient Express", genre="Mystery",
             pages=256, author_id=authors[3].id, published_year=1934, reading_time=8,
             description="Hercule Poirot investigates murder aboard famous train..."),
        Book(title="The A.B.C. Murders", genre="Mystery",
             pages=288, author_id=authors[3].id, published_year=1936, reading_time=9,
             description="Serial killer works through alphabet as Poirot pursues..."),
        Book(title="The Murder of Roger Ackroyd", genre="Mystery", 
             pages=288, author_id=authors[3].id, published_year=1926, reading_time=9,
             description="Classic mystery with famous twist ending..."),
    ]
    db.add_all(books)
    db.commit()
    logger.info(f"Created {len(books)} books")
    return books

def __create_readers(db):
    """Create sample reader profiles with reading preferences."""
    readers = [
        Reader(name="James Bernhardt", email="james.b@example.com", favorite_genre="Mystery"),
        Reader(name="Michael Chen", email="michael@example.com", favorite_genre="Fantasy"),
        Reader(name="Sarah Williams", email="sarah@example.com", favorite_genre="Horror"),
        Reader(name="David Brown", email="david@example.com", favorite_genre="Epic Fantasy"),
        Reader(name="Lisa Garcia", email="lisa@example.com", favorite_genre="Mystery"),
    ]
    db.add_all(readers)
    db.commit()
    logger.info(f"Created {len(readers)} readers")
    return readers

def __create_reading_relationships(db, books, readers):
    """Establish reading relationships between readers and books."""
    relationships = []
    
    # Reader 1: James Bernhardt - Mixed genre reader
    relationships.extend(__book_relationships(books, readers[0], [3, 4, 7, 8, 9, 11, 12, 13, 14]))
    
    # Reader 2: Michael Chen - Fantasy enthusiast  
    relationships.extend(__book_relationships(books, readers[1], range(2, 11)))
    
    # Reader 3: Sarah Williams - Horror fan with some fantasy
    relationships.extend(__book_relationships(books, readers[2], range(7, 11)))
    relationships.extend(__book_relationships(books, readers[2], [1]))
    
    # Reader 4: David Brown - Sanderson specialist
    relationships.extend(__book_relationships(books, readers[3], [3, 5, 6]))
    
    # Reader 5: Lisa Garcia - Mixed genre reader
    relationships.extend(__book_relationships(books, readers[4], [7, 11, 12]))
    
    if relationships:
        db.execute(insert(book_readers), relationships)
        db.commit()
        logger.info(f"Created {len(relationships)} reading relationships")

def __book_relationships(books, reader, indices):
    """Helper to create relationship entries for specified book indices."""
    return [{"book_id": books[i].id, "reader_id": reader.id} for i in indices]
# backend/app/database.py
from sqlalchemy import create_engine, insert
from sqlalchemy.orm import sessionmaker
from .models import Base, Author, Book, Reader, book_readers

# SQLite database
SQLALCHEMY_DATABASE_URL = "sqlite:///./starlibrary.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    Base.metadata.create_all(bind=engine)

def seed_database():
    db = SessionLocal()
    
    try:
        if db.query(Author).count() > 0:
            return  # Already seeded

        print("Seeding database with sample data...")

        # --- Authors ---
        authors = [
            Author(name="J.K. Rowling", bio="British author best known for Harry Potter", nationality="British"),
            Author(name="Brandon Sanderson", bio="American fantasy and science fiction writer", nationality="American"),
            Author(name="Stephen King", bio="American author of horror, supernatural fiction", nationality="American"),
            Author(name="Agatha Christie", bio="English writer known for detective novels", nationality="British"),
        ]
        db.add_all(authors)
        db.flush()

        # --- Books (realistic) ---
        books = [
            Book(title="Harry Potter and the Philosopher's Stone", genre="Fantasy", pages=223, author_id=authors[0].id, published_year=1997, readers_count=1200, reading_time=7),
            Book(title="Harry Potter and the Chamber of Secrets", genre="Fantasy", pages=251, author_id=authors[0].id, published_year=1998, readers_count=1150, reading_time=8),
            Book(title="Harry Potter and the Prisoner of Azkaban", genre="Fantasy", pages=317, author_id=authors[0].id, published_year=1999, readers_count=1100, reading_time=10),
            Book(title="Harry Potter and the Goblet of Fire", genre="Fantasy", pages=636, author_id=authors[0].id, published_year=2000, readers_count=950, reading_time=21),

            Book(title="The Way of Kings", genre="Fantasy", pages=1007, author_id=authors[1].id, published_year=2010, readers_count=600, reading_time=33),
            Book(title="Words of Radiance", genre="Fantasy", pages=1087, author_id=authors[1].id, published_year=2014, readers_count=550, reading_time=36),
            Book(title="Mistborn: The Final Empire", genre="Fantasy", pages=541, author_id=authors[1].id, published_year=2006, readers_count=700, reading_time=18),
            Book(title="Elantris", genre="Fantasy", pages=592, author_id=authors[1].id, published_year=2005, readers_count=400, reading_time=20),

            Book(title="The Shining", genre="Horror", pages=447, author_id=authors[2].id, published_year=1977, readers_count=800, reading_time=15),
            Book(title="It", genre="Horror", pages=1138, author_id=authors[2].id, published_year=1986, readers_count=650, reading_time=38),
            Book(title="The Stand", genre="Horror", pages=1153, author_id=authors[2].id, published_year=1978, readers_count=500, reading_time=39),
            Book(title="Carrie", genre="Horror", pages=199, author_id=authors[2].id, published_year=1974, readers_count=400, reading_time=6),

            Book(title="Murder on the Orient Express", genre="Mystery", pages=256, author_id=authors[3].id, published_year=1934, readers_count=900, reading_time=5),
            Book(title="Death on the Nile", genre="Mystery", pages=288, author_id=authors[3].id, published_year=1937, readers_count=850, reading_time=6),
            Book(title="And Then There Were None", genre="Mystery", pages=272, author_id=authors[3].id, published_year=1939, readers_count=1000, reading_time=6),
        ]
        db.add_all(books)
        db.flush()

        # --- Readers ---
        readers = [
            Reader(name="Emily Johnson", email="emily@email.com", favorite_genre="Fantasy"),
            Reader(name="Michael Chen", email="michael@email.com", favorite_genre="Mystery"),
            Reader(name="Sarah Williams", email="sarah@email.com", favorite_genre="Horror"),
            Reader(name="David Brown", email="david@email.com", favorite_genre="Fantasy"),
            Reader(name="Lisa Garcia", email="lisa@email.com", favorite_genre="Mystery"),
        ]
        db.add_all(readers)
        db.flush()

        # --- Book-Reader Relationships ---
        reading_relationships = []

        # Emily reads most fantasy books
        for book in books[:8]:
            reading_relationships.append({'book_id': book.id, 'reader_id': readers[0].id})

        # Michael reads mystery books
        for book in books[12:15]:
            reading_relationships.append({'book_id': book.id, 'reader_id': readers[1].id})

        # Sarah reads horror books
        for book in books[8:12]:
            reading_relationships.append({'book_id': book.id, 'reader_id': readers[2].id})

        # David reads a mix
        for idx in [0,4,9]:
            reading_relationships.append({'book_id': books[idx].id, 'reader_id': readers[3].id})

        # Lisa reads mystery books
        for book in books[12:15]:
            reading_relationships.append({'book_id': book.id, 'reader_id': readers[4].id})

        db.execute(insert(book_readers), reading_relationships)
        db.commit()

        print("Database seeded successfully with realistic data!")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise e
    finally:
        db.close()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

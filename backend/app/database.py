# backend/app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, Author, Book, Reader, book_readers
from datetime import datetime

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
        # Check if data already exists
        if db.query(Author).count() == 0:
            print("Seeding database with sample data...")
            
            # Create authors
            authors = [
                Author(name="J.K. Rowling", bio="British author best known for Harry Potter", nationality="British"),
                Author(name="Brandon Sanderson", bio="American fantasy and science fiction writer", nationality="American"),
                Author(name="Stephen King", bio="American author of horror, supernatural fiction", nationality="American"),
                Author(name="Agatha Christie", bio="English writer known for detective novels", nationality="British"),
            ]
            db.add_all(authors)
            db.flush()  # Get IDs
            
            # Create books
            books = [
                # J.K. Rowling books
                Book(title="Harry Potter and the Philosopher's Stone", genre="Fantasy", pages=320, author_id=authors[0].id, published_year=1997),
                Book(title="Harry Potter and the Chamber of Secrets", genre="Fantasy", pages=352, author_id=authors[0].id, published_year=1998),
                Book(title="Harry Potter and the Prisoner of Azkaban", genre="Fantasy", pages=435, author_id=authors[0].id, published_year=1999),
                
                # Brandon Sanderson books
                Book(title="The Way of Kings", genre="Fantasy", pages=1007, author_id=authors[1].id, published_year=2010),
                Book(title="Words of Radiance", genre="Fantasy", pages=1087, author_id=authors[1].id, published_year=2014),
                Book(title="Mistborn: The Final Empire", genre="Fantasy", pages=541, author_id=authors[1].id, published_year=2006),
                
                # Stephen King books
                Book(title="The Shining", genre="Horror", pages=447, author_id=authors[2].id, published_year=1977),
                Book(title="It", genre="Horror", pages=1138, author_id=authors[2].id, published_year=1986),
                Book(title="The Stand", genre="Horror", pages=1153, author_id=authors[2].id, published_year=1978),
                
                # Agatha Christie books
                Book(title="Murder on the Orient Express", genre="Mystery", pages=256, author_id=authors[3].id, published_year=1934),
                Book(title="Death on the Nile", genre="Mystery", pages=288, author_id=authors[3].id, published_year=1937),
                Book(title="And Then There Were None", genre="Mystery", pages=272, author_id=authors[3].id, published_year=1939),
            ]
            db.add_all(books)
            db.flush()
            
            # Create readers
            readers = [
                Reader(name="Emily Johnson", email="emily@email.com", favorite_genre="Fantasy"),
                Reader(name="Michael Chen", email="michael@email.com", favorite_genre="Mystery"),
                Reader(name="Sarah Williams", email="sarah@email.com", favorite_genre="Horror"),
                Reader(name="David Brown", email="david@email.com", favorite_genre="Fantasy"),
                Reader(name="Lisa Garcia", email="lisa@email.com", favorite_genre="Mystery"),
            ]
            db.add_all(readers)
            db.flush()
            
            # Create reading relationships (Emily reads most books)
            from sqlalchemy import insert
            reading_relationships = []
            
            # Emily reads books from all authors
            for book in books[:10]:  # Emily reads first 10 books
                reading_relationships.append({
                    'book_id': book.id,
                    'reader_id': readers[0].id  # Emily
                })
            
            # Other readers read random books
            for i, reader in enumerate(readers[1:], 1):
                for book in books[i*2:(i+1)*2]:
                    reading_relationships.append({
                        'book_id': book.id,
                        'reader_id': reader.id
                    })
            
            db.execute(insert(book_readers), reading_relationships)
            db.commit()
            print("Database seeded successfully!")
            
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
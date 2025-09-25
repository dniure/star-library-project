from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Replace USERNAME, PASSWORD, HOST, PORT, DB_NAME with your Postgres values
SQLALCHEMY_DATABASE_URL = "postgresql://USERNAME:PASSWORD@localhost:5432/DB_NAME"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

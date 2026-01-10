# src/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

# Build the connection string
# Format: postgresql://user:password@localhost:port/dbname
DB_URL = "postgresql://user:password@localhost:5432/promobot"

# 1. The Engine: The actual connection to the DB
engine = create_engine(DB_URL)

# 2. The Session: The "holding area" for your changes
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. The Base: The class all your models will inherit from
Base = declarative_base()

def get_db():
    """Helper to get a DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
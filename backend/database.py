import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Fallback default for local development
DEFAULT_LOCAL_DB = "mysql+pymysql://root:@localhost:3306/banagar_db"

DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_LOCAL_DB)

# Create the SQLAlchemy engine for MySQL
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Automatically reconnects if connection drops
    pool_size=10,
    max_overflow=20,
    pool_recycle=3600    # Recycles connections every hour to prevent MySQL timeout errors
)

# Session factory for DB interactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for SQLAlchemy ORM Models
Base = declarative_base()

# FastAPI dependency to yield database sessions cleanly per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
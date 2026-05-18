from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Database Configuration

DATABASE_URL = "sqlite:///./finance.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Required for SQLite + FastAPI
)

# Session Factory

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base Model Class

Base = declarative_base()

# Dependency: Database Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

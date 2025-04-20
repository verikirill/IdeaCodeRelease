import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# SQLite connection parameters
DB_NAME = os.getenv("DB_NAME", "users.db")

# Create SQLAlchemy connection URL for SQLite
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_NAME}"

# Create engine and session
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # Необходимо для SQLite
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

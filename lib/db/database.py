# lib/db/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///project.db"

engine = create_engine(
    DATABASE_URL,
    echo=False,         # set True to see SQL in terminal
    future=True
)

SessionLocal = sessionmaker(
    bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()


def get_session():
    return SessionLocal()

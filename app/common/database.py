import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQLALCHEMY_DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 
                                                    '../../app/app.db')}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

Base.metadata.create_all(bind=engine)


def get_db():
    """
    Provides a database session to interact with the database.

    This function is a generator that yields a new session to interact
    with the database. It automatically closes the session after use,
    ensuring no open connections remain.

    Yields:
        Session: A SQLAlchemy SessionLocal instance for database interaction.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
from pathlib import Path
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker


# ---------------------------------------------------------
# Database file location
# ---------------------------------------------------------

BACKEND_DIR = Path(__file__).resolve().parent
DATABASE_FILE = BACKEND_DIR / "employee_management.db"

DATABASE_URL = f"sqlite:///{DATABASE_FILE.as_posix()}"


# ---------------------------------------------------------
# SQLAlchemy database engine
# ---------------------------------------------------------

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
)


# ---------------------------------------------------------
# Database session
# ---------------------------------------------------------

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# ---------------------------------------------------------
# Base class for database models
# ---------------------------------------------------------

Base = declarative_base()


# ---------------------------------------------------------
# FastAPI database dependency
# ---------------------------------------------------------

def get_db() -> Generator[Session, None, None]:
    """
    Create a database session for each API request.

    The session is automatically closed after the request
    has been completed.
    """

    database = SessionLocal()

    try:
        yield database
    finally:
        database.close()
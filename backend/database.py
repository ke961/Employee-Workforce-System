import os
from pathlib import Path
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker


# ---------------------------------------------------------
# Database file location
# ---------------------------------------------------------

BACKEND_DIR = Path(__file__).resolve().parent
DATABASE_FILE = BACKEND_DIR / "employee_management.db"

# Use DATABASE_URL env var if set (e.g. PostgreSQL on Render),
# otherwise default to the local SQLite file.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{DATABASE_FILE.as_posix()}",
)

# SQLAlchemy requires postgresql:// instead of postgres://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)


# ---------------------------------------------------------
# SQLAlchemy database engine
# ---------------------------------------------------------

# Only SQLite needs check_same_thread=False
_connect_args = (
    {"check_same_thread": False}
    if DATABASE_URL.startswith("sqlite")
    else {}
)

engine = create_engine(
    DATABASE_URL,
    connect_args=_connect_args,
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
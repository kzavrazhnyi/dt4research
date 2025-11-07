"""
Database setup for dt4research (Налаштування бази даних для dt4research).
Uses SQLite with SQLModel and is designed to be swappable to PostgreSQL later
(Використовує SQLite з SQLModel і спроєктована для майбутньої заміни на PostgreSQL).
"""

import os
from contextlib import contextmanager
from typing import Iterator, Optional, Dict, Any

from sqlmodel import Session, SQLModel, create_engine


# Database URL with env override (URL БД з можливістю перевизначення через змінну середовища)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data.db")

# Normalize driver for PostgreSQL to psycopg if needed
if DATABASE_URL.startswith("postgresql://") and "+psycopg" not in DATABASE_URL:
    # Use SQLAlchemy psycopg (v3) driver explicitly (Використати драйвер psycopg v3 явно)
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)

def _build_engine(url: str):
    """Create engine with SQLite-specific connect args (Створити engine з особливими параметрами для SQLite)."""
    connect_args: Optional[Dict[str, Any]] = None
    if url.startswith("sqlite"):
# check_same_thread=False allows usage across threads in Uvicorn reload mode
# (потрібно для режиму перезавантаження Uvicorn)
        connect_args = {"check_same_thread": False}
    return create_engine(url, echo=False, connect_args=connect_args or {})

engine = _build_engine(DATABASE_URL)


def create_db_and_tables() -> None:
    """Create all tables if they do not exist (Створити таблиці, якщо ще не існують)."""
    # Import models to ensure they are registered with SQLModel metadata
    # (Імпортуємо моделі, щоб вони були зареєстровані в метаданих SQLModel)
    from app import db_models  # noqa: F401
    SQLModel.metadata.create_all(engine)


@contextmanager
def get_session() -> Iterator[Session]:
    """Provide a session context manager (Надати контекстний менеджер для сесії)."""
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()



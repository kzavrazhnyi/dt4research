"""
Database setup for dt4research (Налаштування бази даних для dt4research).
Uses SQLite with SQLModel and is designed to be swappable to PostgreSQL later
(Використовує SQLite з SQLModel і спроєктована для майбутньої заміни на PostgreSQL).
"""

from contextlib import contextmanager
from typing import Iterator

from sqlmodel import Session, SQLModel, create_engine


# SQLite file in project root (Файл SQLite у корені проєкту)
DATABASE_URL = "sqlite:///./data.db"

# check_same_thread=False allows usage across threads in Uvicorn reload mode
# (потрібно для режиму перезавантаження Uvicorn)
engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})


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



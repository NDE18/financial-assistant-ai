from sqlmodel import SQLModel, create_engine, Session
from .core.config import settings

# Ensure SQLite works across threads for FastAPI
connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(settings.DATABASE_URL, echo=False, connect_args=connect_args)


def init_db() -> None:
    # Import models so SQLModel can discover them
    from . import models  # noqa: F401
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

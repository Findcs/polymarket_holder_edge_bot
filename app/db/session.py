from collections.abc import Iterator

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

from app.config.settings import get_settings


settings = get_settings()

engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(bind=engine, class_=Session, autoflush=False, autocommit=False)


def get_session() -> Iterator[Session]:
    """Yield a managed SQLAlchemy session."""

    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def check_database_connection() -> bool:
    """Return True when the configured database responds to a trivial query."""

    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return True

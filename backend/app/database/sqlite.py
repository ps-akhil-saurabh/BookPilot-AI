"""
BookPilot AI — SQLite Database Setup

SQLAlchemy engine, session factory, and Base class.
"""

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import settings
from app.core.logger import logger


# ── Engine ───────────────────────────────────────────────────────

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},  # Required for SQLite
    echo=settings.DEBUG,
    pool_pre_ping=True,
)


# Enable SQLite foreign key enforcement
@event.listens_for(engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.execute("PRAGMA journal_mode=WAL")  # Better concurrent performance
    cursor.close()


# ── Session Factory ──────────────────────────────────────────────

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# ── Base Model ───────────────────────────────────────────────────

class Base(DeclarativeBase):
    pass


# ── Dependency ───────────────────────────────────────────────────

def get_db():
    """FastAPI dependency that provides a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ── Initialization ───────────────────────────────────────────────

def init_db():
    """Create all tables defined in the models."""
    # Import all models to register them with Base.metadata
    import app.models.book  # noqa: F401
    import app.models.reading  # noqa: F401
    import app.models.learning  # noqa: F401
    import app.models.analytics  # noqa: F401
    import app.models.memory  # noqa: F401

    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")

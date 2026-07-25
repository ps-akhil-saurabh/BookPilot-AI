"""
BookPilot AI — Book Model

Stores all books in the user's reading library.
Central entity with relationships to progress, sessions, and learning artifacts.
"""

from sqlalchemy import Column, Integer, String, Text, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database.sqlite import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False, index=True)
    author = Column(String(255), nullable=True, index=True)
    genre = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    total_pages = Column(Integer, nullable=False, default=0)
    language = Column(String(50), default="English")
    difficulty = Column(String(20), default="medium")  # easy, medium, hard
    rating = Column(Float, nullable=True)
    cover_url = Column(String(500), nullable=True)
    isbn = Column(String(20), nullable=True)
    file_path = Column(String(500), nullable=True)  # Path to uploaded file
    is_uploaded = Column(Integer, default=0)  # 0 = no file, 1 = uploaded & indexed
    created_at = Column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # ── Relationships ────────────────────────────────────────────
    progress = relationship(
        "Progress",
        back_populates="book",
        uselist=False,
        cascade="all, delete-orphan",
    )
    reading_sessions = relationship(
        "ReadingSession",
        back_populates="book",
        cascade="all, delete-orphan",
    )
    summaries = relationship(
        "Summary", back_populates="book", cascade="all, delete-orphan"
    )
    flashcards = relationship(
        "Flashcard", back_populates="book", cascade="all, delete-orphan"
    )
    quizzes = relationship(
        "Quiz", back_populates="book", cascade="all, delete-orphan"
    )
    vocabulary_items = relationship(
        "Vocabulary", back_populates="book", cascade="all, delete-orphan"
    )
    reflections = relationship(
        "Reflection", back_populates="book", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Book(id={self.id}, title='{self.title}', pages={self.total_pages})>"

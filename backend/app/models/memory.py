"""
BookPilot AI — Memory Models

preferences  — Long-term user reading preferences
memory       — Persistent AI memory (key-value store)
reflections  — User and AI learning reflections
"""

from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database.sqlite import Base


class Preference(Base):
    __tablename__ = "preferences"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    favorite_genre = Column(String(100), nullable=True)
    reading_speed = Column(Float, default=25.0)  # pages per hour
    daily_reading_time = Column(Integer, default=30)  # minutes
    preferred_difficulty = Column(String(20), default="medium")
    preferred_reading_time = Column(
        String(20), nullable=True
    )  # morning, afternoon, evening, night
    weekend_reading_time = Column(Integer, default=60)  # minutes on weekends
    reading_days = Column(
        JSON, default=lambda: ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
    )
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self) -> str:
        return f"<Preference(genre='{self.favorite_genre}', speed={self.reading_speed})>"


class Memory(Base):
    __tablename__ = "memory"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    memory_type = Column(
        String(50), nullable=False, index=True
    )  # preference, habit, insight, conversation
    key = Column(String(100), nullable=False, index=True)
    value = Column(JSON, nullable=True)
    context = Column(Text, nullable=True)  # Additional context for the memory
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self) -> str:
        return f"<Memory(type='{self.memory_type}', key='{self.key}')>"


class Reflection(Base):
    __tablename__ = "reflections"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    book_id = Column(
        Integer,
        ForeignKey("books.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    reflection_type = Column(
        String(50), default="reading"
    )  # reading, plan, session, ai_validation
    reflection = Column(Text, nullable=True)  # User's reflection text
    difficulty_rating = Column(Integer, nullable=True)  # 1-5 scale
    mood = Column(String(50), nullable=True)
    comprehension_rating = Column(Integer, nullable=True)  # 1-5 scale
    ai_feedback = Column(Text, nullable=True)  # AI Reflection Agent's feedback
    ai_approved = Column(Integer, nullable=True)  # 0 = rejected, 1 = approved
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )

    # ── Relationships ────────────────────────────────────────────
    book = relationship("Book", back_populates="reflections")

    def __repr__(self) -> str:
        return f"<Reflection(id={self.id}, type='{self.reflection_type}')>"

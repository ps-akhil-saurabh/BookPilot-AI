"""
BookPilot AI — Analytics Models

analytics       — Aggregated reading statistics
recommendations — AI-generated book recommendations
"""

from sqlalchemy import Column, Integer, String, Text, Float, Date, DateTime
from datetime import datetime, timezone
from app.database.sqlite import Base


class Analytics(Base):
    __tablename__ = "analytics"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    total_books = Column(Integer, default=0)
    completed_books = Column(Integer, default=0)
    total_pages_read = Column(Integer, default=0)
    reading_speed = Column(Float, default=0.0)  # pages per hour
    reading_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    total_reading_minutes = Column(Integer, default=0)
    avg_pages_per_day = Column(Float, default=0.0)
    avg_minutes_per_day = Column(Float, default=0.0)
    predicted_finish = Column(Date, nullable=True)
    last_calculated = Column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self) -> str:
        return f"<Analytics(streak={self.reading_streak}, speed={self.reading_speed})>"


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    recommendation_type = Column(
        String(50), nullable=False
    )  # book, reading_order, mood_based, genre
    book_title = Column(String(255), nullable=True)
    content = Column(Text, nullable=False)
    reason = Column(Text, nullable=True)
    confidence = Column(Float, default=0.0)  # 0.0 - 1.0
    mood = Column(String(50), nullable=True)  # User mood if mood-based
    is_active = Column(Integer, default=1)  # 0 = dismissed, 1 = active
    generated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )

    def __repr__(self) -> str:
        return f"<Recommendation(type='{self.recommendation_type}', confidence={self.confidence})>"

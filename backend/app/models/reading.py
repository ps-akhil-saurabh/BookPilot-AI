"""
BookPilot AI — Reading Models

reading_plans  — AI-generated personalized schedules
reading_sessions — Individual reading activity records
progress — Current reading progress per book
"""

from sqlalchemy import Column, Integer, String, Text, Float, Date, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database.sqlite import Base


class ReadingPlan(Base):
    __tablename__ = "reading_plans"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    plan_name = Column(String(255), nullable=False)
    deadline = Column(Date, nullable=True)
    daily_target_pages = Column(Integer, default=20)
    daily_reading_minutes = Column(Integer, default=30)
    estimated_hours = Column(Float, nullable=True)
    priority_order = Column(JSON, nullable=True)  # Ordered list of book IDs
    book_ids = Column(JSON, nullable=True)  # List of book IDs in this plan
    status = Column(String(20), default="active")  # active, completed, paused, cancelled
    confidence = Column(Float, nullable=True)  # AI confidence score 0.0-1.0
    ai_notes = Column(Text, nullable=True)  # AI reasoning and notes
    schedule_data = Column(JSON, nullable=True)  # Day-by-day schedule
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # ── Relationships ────────────────────────────────────────────
    sessions = relationship(
        "ReadingSession", back_populates="plan", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<ReadingPlan(id={self.id}, name='{self.plan_name}', status='{self.status}')>"


class ReadingSession(Base):
    __tablename__ = "reading_sessions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    book_id = Column(
        Integer,
        ForeignKey("books.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    plan_id = Column(
        Integer,
        ForeignKey("reading_plans.id", ondelete="SET NULL"),
        nullable=True,
    )
    session_date = Column(Date, nullable=False, index=True)
    pages_read = Column(Integer, default=0)
    duration_minutes = Column(Integer, default=0)
    start_page = Column(Integer, nullable=True)
    end_page = Column(Integer, nullable=True)
    chapter = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # ── Relationships ────────────────────────────────────────────
    book = relationship("Book", back_populates="reading_sessions")
    plan = relationship("ReadingPlan", back_populates="sessions")

    def __repr__(self) -> str:
        return f"<ReadingSession(id={self.id}, book_id={self.book_id}, pages={self.pages_read})>"


class Progress(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    book_id = Column(
        Integer,
        ForeignKey("books.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )
    current_page = Column(Integer, default=0)
    percentage = Column(Float, default=0.0)
    completed = Column(Integer, default=0)  # 0 = in progress, 1 = completed
    last_read_date = Column(Date, nullable=True)
    last_updated = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # ── Relationships ────────────────────────────────────────────
    book = relationship("Book", back_populates="progress")

    def __repr__(self) -> str:
        return f"<Progress(book_id={self.book_id}, page={self.current_page}, {self.percentage:.1f}%)>"

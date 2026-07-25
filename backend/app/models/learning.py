"""
BookPilot AI — Learning Models

summaries   — AI-generated chapter summaries
flashcards  — Revision cards from book content
quizzes     — MCQ, True/False, and short answer questions
vocabulary  — Unfamiliar words with meanings and examples
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database.sqlite import Base


class Summary(Base):
    __tablename__ = "summaries"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    book_id = Column(
        Integer,
        ForeignKey("books.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    chapter = Column(String(100), nullable=True, index=True)
    summary = Column(Text, nullable=False)
    key_points = Column(JSON, nullable=True)  # List of key takeaways
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    book = relationship("Book", back_populates="summaries")

    def __repr__(self) -> str:
        return f"<Summary(book_id={self.book_id}, chapter='{self.chapter}')>"


class Flashcard(Base):
    __tablename__ = "flashcards"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    book_id = Column(
        Integer,
        ForeignKey("books.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    chapter = Column(String(100), nullable=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    difficulty = Column(String(20), default="medium")
    times_reviewed = Column(Integer, default=0)
    last_reviewed = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    book = relationship("Book", back_populates="flashcards")

    def __repr__(self) -> str:
        return f"<Flashcard(id={self.id}, book_id={self.book_id})>"


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    book_id = Column(
        Integer,
        ForeignKey("books.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    chapter = Column(String(100), nullable=True)
    question = Column(Text, nullable=False)
    question_type = Column(String(20), default="mcq")  # mcq, true_false, short_answer
    options = Column(JSON, nullable=True)  # List of option strings (for MCQ)
    answer = Column(String(500), nullable=False)
    explanation = Column(Text, nullable=True)
    user_answer = Column(String(500), nullable=True)
    is_correct = Column(Integer, nullable=True)  # 0 = wrong, 1 = correct, NULL = unanswered
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    book = relationship("Book", back_populates="quizzes")

    def __repr__(self) -> str:
        return f"<Quiz(id={self.id}, type='{self.question_type}', book_id={self.book_id})>"


class Vocabulary(Base):
    __tablename__ = "vocabulary"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    book_id = Column(
        Integer,
        ForeignKey("books.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    word = Column(String(100), nullable=False, index=True)
    meaning = Column(Text, nullable=False)
    example = Column(Text, nullable=True)
    context = Column(Text, nullable=True)  # Original context from book
    mastered = Column(Integer, default=0)  # 0 = learning, 1 = mastered
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    book = relationship("Book", back_populates="vocabulary_items")

    def __repr__(self) -> str:
        return f"<Vocabulary(word='{self.word}', mastered={bool(self.mastered)})>"

"""
BookPilot AI — Learning Repository

Domain-specific queries for summaries, flashcards, quizzes, and vocabulary.
"""

from typing import Optional, Sequence
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.learning import Summary, Flashcard, Quiz, Vocabulary
from app.database.repositories.base import BaseRepository


class SummaryRepository(BaseRepository[Summary]):
    def __init__(self, db: Session):
        super().__init__(Summary, db)

    def get_by_book(self, book_id: int) -> Sequence[Summary]:
        """Get all summaries for a book."""
        return (
            self.db.query(Summary)
            .filter(Summary.book_id == book_id)
            .order_by(Summary.created_at)
            .all()
        )

    def get_by_chapter(self, book_id: int, chapter: str) -> Optional[Summary]:
        """Get summary for a specific chapter."""
        return (
            self.db.query(Summary)
            .filter(Summary.book_id == book_id, Summary.chapter == chapter)
            .first()
        )


class FlashcardRepository(BaseRepository[Flashcard]):
    def __init__(self, db: Session):
        super().__init__(Flashcard, db)

    def get_by_book(self, book_id: int) -> Sequence[Flashcard]:
        """Get all flashcards for a book."""
        return (
            self.db.query(Flashcard)
            .filter(Flashcard.book_id == book_id)
            .order_by(Flashcard.created_at)
            .all()
        )

    def get_for_review(self, book_id: int, limit: int = 20) -> Sequence[Flashcard]:
        """Get flashcards that need review (least recently reviewed first)."""
        return (
            self.db.query(Flashcard)
            .filter(Flashcard.book_id == book_id)
            .order_by(Flashcard.last_reviewed.asc().nullsfirst())
            .limit(limit)
            .all()
        )


class QuizRepository(BaseRepository[Quiz]):
    def __init__(self, db: Session):
        super().__init__(Quiz, db)

    def get_by_book(self, book_id: int) -> Sequence[Quiz]:
        """Get all quizzes for a book."""
        return (
            self.db.query(Quiz)
            .filter(Quiz.book_id == book_id)
            .order_by(Quiz.created_at)
            .all()
        )

    def get_by_chapter(self, book_id: int, chapter: str) -> Sequence[Quiz]:
        """Get quizzes for a specific chapter."""
        return (
            self.db.query(Quiz)
            .filter(Quiz.book_id == book_id, Quiz.chapter == chapter)
            .all()
        )

    def get_unanswered(self, book_id: int) -> Sequence[Quiz]:
        """Get all unanswered quizzes for a book."""
        return (
            self.db.query(Quiz)
            .filter(Quiz.book_id == book_id, Quiz.user_answer.is_(None))
            .all()
        )

    def get_score(self, book_id: int) -> dict:
        """Get quiz score for a book."""
        total = self.db.query(Quiz).filter(Quiz.book_id == book_id).count()
        answered = (
            self.db.query(Quiz)
            .filter(Quiz.book_id == book_id, Quiz.user_answer.isnot(None))
            .count()
        )
        correct = (
            self.db.query(Quiz)
            .filter(Quiz.book_id == book_id, Quiz.is_correct == 1)
            .count()
        )
        return {
            "total": total,
            "answered": answered,
            "correct": correct,
            "percentage": round((correct / answered * 100) if answered > 0 else 0, 1),
        }


class VocabularyRepository(BaseRepository[Vocabulary]):
    def __init__(self, db: Session):
        super().__init__(Vocabulary, db)

    def get_by_book(self, book_id: int) -> Sequence[Vocabulary]:
        """Get all vocabulary for a book."""
        return (
            self.db.query(Vocabulary)
            .filter(Vocabulary.book_id == book_id)
            .order_by(Vocabulary.created_at)
            .all()
        )

    def get_unmastered(self, book_id: int = None) -> Sequence[Vocabulary]:
        """Get all unmastered vocabulary words."""
        query = self.db.query(Vocabulary).filter(Vocabulary.mastered == 0)
        if book_id:
            query = query.filter(Vocabulary.book_id == book_id)
        return query.all()

    def search_word(self, word: str) -> Optional[Vocabulary]:
        """Search for a specific word."""
        return (
            self.db.query(Vocabulary)
            .filter(Vocabulary.word.ilike(word))
            .first()
        )

"""
BookPilot AI — Learning Schemas

Request/response models for learning features: questions, summaries, quizzes, flashcards, vocabulary.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# ── Question / Explanation ───────────────────────────────────────

class QuestionRequest(BaseModel):
    """POST /api/v1/learning/question — request body."""
    book_id: int
    question: str = Field(..., min_length=1, max_length=2000)
    chapter: Optional[str] = None


class QuestionResponse(BaseModel):
    """AI-generated answer response."""
    answer: str
    sources: Optional[list[str]] = None  # Source chunks used
    confidence: Optional[float] = None
    grounded: bool = True  # Whether answer is grounded in uploaded content


# ── Summary ──────────────────────────────────────────────────────

class SummaryRequest(BaseModel):
    """POST /api/v1/learning/summary — request body."""
    book_id: int
    chapter: Optional[str] = None


class SummaryResponse(BaseModel):
    """Chapter summary response."""
    id: int
    book_id: int
    chapter: Optional[str] = None
    summary: str
    key_points: Optional[list[str]] = None
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Quiz ─────────────────────────────────────────────────────────

class QuizGenerateRequest(BaseModel):
    """POST /api/v1/learning/quiz — request body."""
    book_id: int
    chapter: Optional[str] = None
    num_questions: int = Field(5, ge=1, le=20)
    question_types: Optional[list[str]] = None  # mcq, true_false, short_answer


class QuizQuestionResponse(BaseModel):
    """Single quiz question."""
    id: int
    question: str
    question_type: str
    options: Optional[list[str]] = None
    book_id: int
    chapter: Optional[str] = None

    model_config = {"from_attributes": True}


class QuizAnswerRequest(BaseModel):
    """Submit a quiz answer."""
    quiz_id: int
    answer: str


class QuizAnswerResponse(BaseModel):
    """Quiz answer result."""
    quiz_id: int
    correct: bool
    correct_answer: str
    explanation: Optional[str] = None


class QuizScoreResponse(BaseModel):
    """Quiz score for a book."""
    total: int
    answered: int
    correct: int
    percentage: float


# ── Flashcards ───────────────────────────────────────────────────

class FlashcardGenerateRequest(BaseModel):
    """POST /api/v1/learning/flashcards — request body."""
    book_id: int
    chapter: Optional[str] = None
    num_cards: int = Field(10, ge=1, le=50)


class FlashcardResponse(BaseModel):
    """Single flashcard response."""
    id: int
    book_id: int
    chapter: Optional[str] = None
    question: str
    answer: str
    difficulty: str
    times_reviewed: int = 0

    model_config = {"from_attributes": True}


# ── Vocabulary ───────────────────────────────────────────────────

class VocabularyResponse(BaseModel):
    """Vocabulary word response."""
    id: int
    book_id: int
    word: str
    meaning: str
    example: Optional[str] = None
    context: Optional[str] = None
    mastered: bool = False

    model_config = {"from_attributes": True}


class VocabularyAddRequest(BaseModel):
    """Manually add a vocabulary word."""
    book_id: int
    word: str = Field(..., min_length=1, max_length=100)
    meaning: Optional[str] = None

"""
BookPilot AI — Learning API

RAG-powered Q&A, summaries, quizzes, flashcards, and vocabulary.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.database.sqlite import get_db
from app.schemas.learning import (
    QuestionRequest, QuestionResponse, SummaryRequest, SummaryResponse,
    QuizGenerateRequest, QuizQuestionResponse, FlashcardGenerateRequest, FlashcardResponse
)
from app.schemas.common import StandardResponse
from app.agents.learning_agent import learning_agent
from app.database.repositories.learning_repository import FlashcardRepository, QuizRepository, VocabularyRepository

router = APIRouter()

@router.post("/learning/question", response_model=QuestionResponse)
async def ask_question(req: QuestionRequest):
    """Ask a question about an uploaded book (RAG)."""
    res = await learning_agent.answer_question(req.question, book_id=req.book_id)
    return QuestionResponse(
        answer=res["answer"],
        sources=res["sources"],
        grounded=res["grounded"],
    )

@router.post("/learning/summary")
async def generate_summary(req: SummaryRequest):
    """Generate chapter summary."""
    res = await learning_agent.generate_summary(f"Chapter overview for book {req.book_id}")
    return StandardResponse(
        message="Summary generated successfully.",
        data={"summary": res["summary"]},
        timestamp=datetime.now(timezone.utc),
    )

@router.post("/learning/quiz")
async def generate_quiz(req: QuizGenerateRequest, db: Session = Depends(get_db)):
    """Generate quiz questions."""
    repo = QuizRepository(db)
    quiz_item = repo.create({
        "book_id": req.book_id,
        "chapter": req.chapter or "Chapter 1",
        "question": "What is the core habit loop described in the book?",
        "question_type": "mcq",
        "options": ["Trigger, Craving, Response, Reward", "Plan, Do, Check, Act", "Read, Note, Review, Repeat"],
        "answer": "Trigger, Craving, Response, Reward",
        "explanation": "Habit loop consists of cue/trigger, craving, response, and reward.",
    })
    return StandardResponse(
        message="Quiz generated.",
        data={"questions": [{"id": quiz_item.id, "question": quiz_item.question, "options": quiz_item.options}]},
        timestamp=datetime.now(timezone.utc),
    )

@router.get("/learning/vocabulary")
async def get_vocabulary(db: Session = Depends(get_db)):
    """Get learned vocabulary words."""
    repo = VocabularyRepository(db)
    items = repo.get_all()
    return StandardResponse(
        data=[{"id": v.id, "word": v.word, "meaning": v.meaning, "mastered": bool(v.mastered)} for v in items]
    )

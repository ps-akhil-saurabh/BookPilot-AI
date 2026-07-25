"""
BookPilot AI — Reading & Schedule API

Endpoints for tracking daily reading progress and schedule queries.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date, datetime, timezone

from app.database.sqlite import get_db
from app.database.repositories import ProgressRepository, ReadingSessionRepository, BookRepository
from app.schemas.reading import ProgressUpdate, ProgressResponse, SessionCreate, SessionResponse, TodayScheduleResponse
from app.schemas.common import StandardResponse
from app.core.exceptions import BookNotFoundException

router = APIRouter()

@router.post("/reading/progress")
async def update_progress(data: ProgressUpdate, db: Session = Depends(get_db)):
    """Update current page and log reading session."""
    book_repo = BookRepository(db)
    book = book_repo.get_by_id(data.book_id)
    if not book:
        raise BookNotFoundException(data.book_id)

    # Update progress
    progress_repo = ProgressRepository(db)
    progress = progress_repo.upsert(data.book_id, data.current_page, book.total_pages)

    # Record reading session
    session_repo = ReadingSessionRepository(db)
    session_repo.create({
        "book_id": data.book_id,
        "session_date": date.today(),
        "pages_read": max(0, data.current_page - progress.current_page),
        "duration_minutes": data.minutes or 20,
        "chapter": data.chapter,
        "notes": data.notes,
    })

    return StandardResponse(
        message="Reading progress updated.",
        data={
            "book_id": data.book_id,
            "current_page": progress.current_page,
            "percentage": progress.percentage,
            "completed": bool(progress.completed),
        },
        timestamp=datetime.now(timezone.utc),
    )

@router.get("/schedule/today", response_model=TodayScheduleResponse)
async def get_today_schedule(db: Session = Depends(get_db)):
    """Get today's target reading task."""
    book_repo = BookRepository(db)
    books = book_repo.get_all(limit=1)
    if not books:
        return TodayScheduleResponse(
            pages=20, estimated_minutes=30, book="No active book", book_id=0, progress_percentage=0.0
        )

    book = books[0]
    progress_repo = ProgressRepository(db)
    progress = progress_repo.get_by_book_id(book.id)

    return TodayScheduleResponse(
        pages=22,
        estimated_minutes=35,
        book=book.title,
        book_id=book.id,
        progress_percentage=progress.percentage if progress else 0.0,
    )

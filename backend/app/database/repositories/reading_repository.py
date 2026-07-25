"""
BookPilot AI — Reading Repository

Domain-specific queries for reading_plans, reading_sessions, and progress.
"""

from typing import Optional, Sequence
from datetime import date, datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.models.reading import ReadingPlan, ReadingSession, Progress
from app.database.repositories.base import BaseRepository


class ReadingPlanRepository(BaseRepository[ReadingPlan]):
    def __init__(self, db: Session):
        super().__init__(ReadingPlan, db)

    def get_active_plans(self) -> Sequence[ReadingPlan]:
        """Get all active reading plans."""
        return (
            self.db.query(ReadingPlan)
            .filter(ReadingPlan.status == "active")
            .order_by(desc(ReadingPlan.created_at))
            .all()
        )

    def get_latest_plan(self) -> Optional[ReadingPlan]:
        """Get the most recently created plan."""
        return (
            self.db.query(ReadingPlan)
            .order_by(desc(ReadingPlan.created_at))
            .first()
        )


class ReadingSessionRepository(BaseRepository[ReadingSession]):
    def __init__(self, db: Session):
        super().__init__(ReadingSession, db)

    def get_sessions_by_book(
        self, book_id: int, limit: int = 50
    ) -> Sequence[ReadingSession]:
        """Get reading sessions for a specific book."""
        return (
            self.db.query(ReadingSession)
            .filter(ReadingSession.book_id == book_id)
            .order_by(desc(ReadingSession.session_date))
            .limit(limit)
            .all()
        )

    def get_sessions_by_date(self, target_date: date) -> Sequence[ReadingSession]:
        """Get all reading sessions for a specific date."""
        return (
            self.db.query(ReadingSession)
            .filter(ReadingSession.session_date == target_date)
            .all()
        )

    def get_sessions_in_range(
        self, start_date: date, end_date: date
    ) -> Sequence[ReadingSession]:
        """Get all sessions within a date range."""
        return (
            self.db.query(ReadingSession)
            .filter(
                ReadingSession.session_date >= start_date,
                ReadingSession.session_date <= end_date,
            )
            .order_by(ReadingSession.session_date)
            .all()
        )

    def get_total_pages_by_book(self, book_id: int) -> int:
        """Get total pages read for a specific book."""
        result = (
            self.db.query(func.sum(ReadingSession.pages_read))
            .filter(ReadingSession.book_id == book_id)
            .scalar()
        )
        return result or 0

    def get_total_minutes_by_book(self, book_id: int) -> int:
        """Get total reading minutes for a specific book."""
        result = (
            self.db.query(func.sum(ReadingSession.duration_minutes))
            .filter(ReadingSession.book_id == book_id)
            .scalar()
        )
        return result or 0

    def get_recent_sessions(self, limit: int = 10) -> Sequence[ReadingSession]:
        """Get the most recent reading sessions."""
        return (
            self.db.query(ReadingSession)
            .order_by(desc(ReadingSession.session_date))
            .limit(limit)
            .all()
        )

    def get_reading_dates(self, days: int = 365) -> Sequence[date]:
        """Get all dates where reading occurred (for streak/heatmap)."""
        results = (
            self.db.query(ReadingSession.session_date)
            .distinct()
            .order_by(desc(ReadingSession.session_date))
            .limit(days)
            .all()
        )
        return [r[0] for r in results]


class ProgressRepository(BaseRepository[Progress]):
    def __init__(self, db: Session):
        super().__init__(Progress, db)

    def get_by_book_id(self, book_id: int) -> Optional[Progress]:
        """Get progress for a specific book."""
        return (
            self.db.query(Progress)
            .filter(Progress.book_id == book_id)
            .first()
        )

    def upsert(self, book_id: int, current_page: int, total_pages: int) -> Progress:
        """Create or update progress for a book."""
        progress = self.get_by_book_id(book_id)
        percentage = (current_page / total_pages * 100) if total_pages > 0 else 0
        completed = 1 if current_page >= total_pages else 0

        if progress is None:
            progress = Progress(
                book_id=book_id,
                current_page=current_page,
                percentage=round(percentage, 1),
                completed=completed,
                last_read_date=date.today(),
            )
            self.db.add(progress)
        else:
            progress.current_page = current_page
            progress.percentage = round(percentage, 1)
            progress.completed = completed
            progress.last_read_date = date.today()
            progress.last_updated = datetime.now(timezone.utc)

        self.db.commit()
        self.db.refresh(progress)
        return progress

    def get_completed_books(self) -> Sequence[Progress]:
        """Get progress records for all completed books."""
        return (
            self.db.query(Progress)
            .filter(Progress.completed == 1)
            .all()
        )

    def get_in_progress_books(self) -> Sequence[Progress]:
        """Get progress records for all in-progress books."""
        return (
            self.db.query(Progress)
            .filter(Progress.completed == 0, Progress.current_page > 0)
            .all()
        )

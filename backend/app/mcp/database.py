"""
BookPilot AI — Database MCP Tool Integration

Queries persistent application data (reading history, preferences, analytics) for AI agents.
"""

from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.core.logger import get_mcp_logger
from app.database.repositories.reading_repository import ReadingSessionRepository, ProgressRepository
from app.database.repositories.analytics_repository import PreferenceRepository, AnalyticsRepository

logger = get_mcp_logger("DatabaseMCP")

class DatabaseMCP:
    """Database MCP tool for agents to read historical data."""

    def get_user_reading_profile(self, db: Session) -> Dict[str, Any]:
        """Fetch user preferences, reading speed, and current stats."""
        pref_repo = PreferenceRepository(db)
        analytics_repo = AnalyticsRepository(db)
        
        pref = pref_repo.get_current()
        analytics = analytics_repo.get_latest()

        return {
            "favorite_genre": pref.favorite_genre if pref else "General",
            "reading_speed": pref.reading_speed if pref else 25.0,
            "daily_reading_time": pref.daily_reading_time if pref else 30,
            "preferred_difficulty": pref.preferred_difficulty if pref else "medium",
            "reading_streak": analytics.reading_streak if analytics else 0,
            "total_books_completed": analytics.completed_books if analytics else 0,
        }

    def get_recent_activity(self, db: Session, days: int = 7) -> List[Dict[str, Any]]:
        """Fetch recent reading sessions."""
        session_repo = ReadingSessionRepository(db)
        sessions = session_repo.get_recent_sessions(limit=days)
        return [
            {
                "book_id": s.book_id,
                "session_date": s.session_date.isoformat(),
                "pages_read": s.pages_read,
                "duration_minutes": s.duration_minutes,
            }
            for s in sessions
        ]

database_mcp = DatabaseMCP()

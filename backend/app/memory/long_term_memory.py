"""
BookPilot AI — Long-Term Memory Module

Persists user preferences, reading habits, and AI learnings in SQLite.
"""

from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from app.database.repositories.analytics_repository import PreferenceRepository, MemoryRepository

class LongTermMemoryManager:
    """Manages persistent memory and user preferences."""

    def get_preferences(self, db: Session) -> Dict[str, Any]:
        repo = PreferenceRepository(db)
        pref = repo.get_current()
        if not pref:
            return {
                "favorite_genre": "General",
                "reading_speed": 25.0,
                "daily_reading_time": 30,
                "preferred_difficulty": "medium",
            }
        return {
            "favorite_genre": pref.favorite_genre,
            "reading_speed": pref.reading_speed,
            "daily_reading_time": pref.daily_reading_time,
            "preferred_difficulty": pref.preferred_difficulty,
            "weekend_reading_time": pref.weekend_reading_time,
            "reading_days": pref.reading_days,
        }

    def update_preferences(self, db: Session, data: Dict[str, Any]):
        repo = PreferenceRepository(db)
        return repo.upsert(data)

    def store_insight(self, db: Session, key: str, value: Dict[str, Any], context: str = None):
        repo = MemoryRepository(db)
        return repo.upsert("insight", key, value, context)

    def get_insights(self, db: Session) -> Dict[str, Any]:
        repo = MemoryRepository(db)
        memories = repo.get_by_type("insight")
        return {m.key: m.value for m in memories}

long_term_memory = LongTermMemoryManager()

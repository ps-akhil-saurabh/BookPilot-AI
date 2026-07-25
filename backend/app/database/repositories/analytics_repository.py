"""
BookPilot AI — Analytics & Memory Repositories

analytics_repository   — Aggregated reading statistics
memory_repository      — Preferences, AI memory, reflections
"""

from typing import Optional, Sequence
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.analytics import Analytics, Recommendation
from app.models.memory import Preference, Memory, Reflection
from app.database.repositories.base import BaseRepository


# ── Analytics ────────────────────────────────────────────────────

class AnalyticsRepository(BaseRepository[Analytics]):
    def __init__(self, db: Session):
        super().__init__(Analytics, db)

    def get_latest(self) -> Optional[Analytics]:
        """Get the most recent analytics snapshot."""
        return (
            self.db.query(Analytics)
            .order_by(desc(Analytics.last_calculated))
            .first()
        )

    def upsert(self, data: dict) -> Analytics:
        """Create or update the analytics record."""
        existing = self.get_latest()
        if existing:
            for key, value in data.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)
            self.db.commit()
            self.db.refresh(existing)
            return existing
        else:
            return self.create(data)


class RecommendationRepository(BaseRepository[Recommendation]):
    def __init__(self, db: Session):
        super().__init__(Recommendation, db)

    def get_active(self, limit: int = 5) -> Sequence[Recommendation]:
        """Get active (non-dismissed) recommendations."""
        return (
            self.db.query(Recommendation)
            .filter(Recommendation.is_active == 1)
            .order_by(desc(Recommendation.generated_at))
            .limit(limit)
            .all()
        )

    def get_by_type(self, rec_type: str) -> Sequence[Recommendation]:
        """Get recommendations of a specific type."""
        return (
            self.db.query(Recommendation)
            .filter(Recommendation.recommendation_type == rec_type)
            .order_by(desc(Recommendation.generated_at))
            .all()
        )


# ── Memory ───────────────────────────────────────────────────────

class PreferenceRepository(BaseRepository[Preference]):
    def __init__(self, db: Session):
        super().__init__(Preference, db)

    def get_current(self) -> Optional[Preference]:
        """Get the current user preferences (single-user V1)."""
        return self.db.query(Preference).first()

    def upsert(self, data: dict) -> Preference:
        """Create or update user preferences."""
        existing = self.get_current()
        if existing:
            for key, value in data.items():
                if value is not None and hasattr(existing, key):
                    setattr(existing, key, value)
            self.db.commit()
            self.db.refresh(existing)
            return existing
        else:
            return self.create(data)


class MemoryRepository(BaseRepository[Memory]):
    def __init__(self, db: Session):
        super().__init__(Memory, db)

    def get_by_key(self, key: str) -> Optional[Memory]:
        """Get a memory entry by key."""
        return (
            self.db.query(Memory)
            .filter(Memory.key == key)
            .first()
        )

    def get_by_type(self, memory_type: str) -> Sequence[Memory]:
        """Get all memory entries of a specific type."""
        return (
            self.db.query(Memory)
            .filter(Memory.memory_type == memory_type)
            .all()
        )

    def upsert(self, memory_type: str, key: str, value: dict, context: str = None) -> Memory:
        """Create or update a memory entry by key."""
        existing = self.get_by_key(key)
        if existing:
            existing.value = value
            existing.memory_type = memory_type
            if context:
                existing.context = context
            self.db.commit()
            self.db.refresh(existing)
            return existing
        else:
            return self.create({
                "memory_type": memory_type,
                "key": key,
                "value": value,
                "context": context,
            })


class ReflectionRepository(BaseRepository[Reflection]):
    def __init__(self, db: Session):
        super().__init__(Reflection, db)

    def get_by_book(self, book_id: int) -> Sequence[Reflection]:
        """Get all reflections for a book."""
        return (
            self.db.query(Reflection)
            .filter(Reflection.book_id == book_id)
            .order_by(desc(Reflection.created_at))
            .all()
        )

    def get_recent(self, limit: int = 10) -> Sequence[Reflection]:
        """Get the most recent reflections."""
        return (
            self.db.query(Reflection)
            .order_by(desc(Reflection.created_at))
            .limit(limit)
            .all()
        )

    def get_ai_reflections(self, limit: int = 10) -> Sequence[Reflection]:
        """Get AI validation reflections."""
        return (
            self.db.query(Reflection)
            .filter(Reflection.reflection_type == "ai_validation")
            .order_by(desc(Reflection.created_at))
            .limit(limit)
            .all()
        )

"""
BookPilot AI — Base Repository

Generic repository pattern providing CRUD operations.
All specific repositories inherit from this base.
"""

from typing import TypeVar, Generic, Type, Optional, Sequence
from sqlalchemy.orm import Session
from app.database.sqlite import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Base CRUD repository.

    Provides: get_by_id, get_all, create, update, delete, count.
    Subclasses add domain-specific queries.
    """

    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db

    def get_by_id(self, id: int) -> Optional[ModelType]:
        """Get a single record by primary key."""
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> Sequence[ModelType]:
        """Get all records with pagination."""
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def create(self, obj_data: dict) -> ModelType:
        """Create a new record from a dictionary."""
        db_obj = self.model(**obj_data)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(self, id: int, obj_data: dict) -> Optional[ModelType]:
        """Update an existing record. Returns None if not found."""
        db_obj = self.get_by_id(id)
        if db_obj is None:
            return None
        for key, value in obj_data.items():
            if value is not None and hasattr(db_obj, key):
                setattr(db_obj, key, value)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def delete(self, id: int) -> bool:
        """Delete a record by primary key. Returns True if deleted."""
        db_obj = self.get_by_id(id)
        if db_obj is None:
            return False
        self.db.delete(db_obj)
        self.db.commit()
        return True

    def count(self) -> int:
        """Count total records."""
        return self.db.query(self.model).count()

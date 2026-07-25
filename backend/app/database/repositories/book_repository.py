"""
BookPilot AI — Book Repository

Domain-specific queries for the books table.
"""

from typing import Optional, Sequence
from sqlalchemy.orm import Session
from app.models.book import Book
from app.database.repositories.base import BaseRepository


class BookRepository(BaseRepository[Book]):
    def __init__(self, db: Session):
        super().__init__(Book, db)

    def get_by_title(self, title: str) -> Optional[Book]:
        """Find a book by exact title match (case-insensitive)."""
        return (
            self.db.query(Book)
            .filter(Book.title.ilike(title))
            .first()
        )

    def search(self, query: str, skip: int = 0, limit: int = 20) -> Sequence[Book]:
        """Search books by title or author."""
        pattern = f"%{query}%"
        return (
            self.db.query(Book)
            .filter(
                (Book.title.ilike(pattern)) | (Book.author.ilike(pattern))
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_genre(self, genre: str) -> Sequence[Book]:
        """Get all books in a specific genre."""
        return (
            self.db.query(Book)
            .filter(Book.genre.ilike(f"%{genre}%"))
            .all()
        )

    def get_by_difficulty(self, difficulty: str) -> Sequence[Book]:
        """Get all books of a specific difficulty."""
        return (
            self.db.query(Book)
            .filter(Book.difficulty == difficulty)
            .all()
        )

    def get_uploaded_books(self) -> Sequence[Book]:
        """Get all books that have been uploaded (have file content)."""
        return (
            self.db.query(Book)
            .filter(Book.is_uploaded == 1)
            .all()
        )

    def get_by_ids(self, ids: list[int]) -> Sequence[Book]:
        """Get multiple books by a list of IDs."""
        return (
            self.db.query(Book)
            .filter(Book.id.in_(ids))
            .all()
        )

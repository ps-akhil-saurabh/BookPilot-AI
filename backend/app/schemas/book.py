"""
BookPilot AI — Book Schemas

Request/response models for the Books API.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class BookCreate(BaseModel):
    """POST /api/v1/books — request body."""
    title: str = Field(..., min_length=1, max_length=255, examples=["Atomic Habits"])
    author: Optional[str] = Field(None, max_length=255, examples=["James Clear"])
    genre: Optional[str] = Field(None, max_length=100, examples=["Self Help"])
    total_pages: Optional[int] = Field(None, gt=0, examples=[320])
    description: Optional[str] = None
    language: Optional[str] = Field("English", max_length=50)
    difficulty: Optional[str] = Field("medium", pattern="^(easy|medium|hard)$")
    cover_url: Optional[str] = None
    isbn: Optional[str] = Field(None, max_length=20)


class BookUpdate(BaseModel):
    """PUT /api/v1/books/{book_id} — request body."""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    author: Optional[str] = Field(None, max_length=255)
    genre: Optional[str] = Field(None, max_length=100)
    total_pages: Optional[int] = Field(None, gt=0)
    description: Optional[str] = None
    language: Optional[str] = None
    difficulty: Optional[str] = Field(None, pattern="^(easy|medium|hard)$")
    rating: Optional[float] = Field(None, ge=0, le=5)
    cover_url: Optional[str] = None
    isbn: Optional[str] = None


class BookResponse(BaseModel):
    """Full book detail response."""
    id: int
    title: str
    author: Optional[str] = None
    genre: Optional[str] = None
    description: Optional[str] = None
    total_pages: int
    language: str = "English"
    difficulty: str = "medium"
    rating: Optional[float] = None
    cover_url: Optional[str] = None
    isbn: Optional[str] = None
    is_uploaded: bool = False
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class BookListItem(BaseModel):
    """Compact book representation for list views."""
    id: int
    title: str
    author: Optional[str] = None
    genre: Optional[str] = None
    total_pages: int
    difficulty: str = "medium"
    rating: Optional[float] = None
    is_uploaded: bool = False
    progress: Optional[float] = 0.0  # Percentage complete

    model_config = {"from_attributes": True}

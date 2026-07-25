"""
BookPilot AI — Reading Schemas

Request/response models for reading progress and plans.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime


# ── Progress ─────────────────────────────────────────────────────

class ProgressUpdate(BaseModel):
    """POST /api/v1/reading/progress — request body."""
    book_id: int
    current_page: int = Field(..., ge=0)
    minutes: Optional[int] = Field(None, ge=0)
    chapter: Optional[str] = None
    notes: Optional[str] = None


class ProgressResponse(BaseModel):
    """Reading progress response."""
    id: int
    book_id: int
    current_page: int
    percentage: float
    completed: bool
    last_read_date: Optional[date] = None
    last_updated: datetime

    model_config = {"from_attributes": True}


# ── Reading Sessions ─────────────────────────────────────────────

class SessionCreate(BaseModel):
    """Create a reading session record."""
    book_id: int
    session_date: date
    pages_read: int = Field(..., ge=0)
    duration_minutes: int = Field(0, ge=0)
    start_page: Optional[int] = None
    end_page: Optional[int] = None
    chapter: Optional[str] = None
    notes: Optional[str] = None


class SessionResponse(BaseModel):
    """Reading session response."""
    id: int
    book_id: int
    plan_id: Optional[int] = None
    session_date: date
    pages_read: int
    duration_minutes: int
    chapter: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Reading Plans ────────────────────────────────────────────────

class PlanCreate(BaseModel):
    """POST /api/v1/planner/generate — request body."""
    book_ids: list[int] = Field(..., min_length=1)
    deadline: Optional[date] = None
    daily_minutes: int = Field(30, ge=5, le=480)
    plan_name: Optional[str] = None


class PlanReplan(BaseModel):
    """POST /api/v1/planner/replan — request body."""
    plan_id: int
    missed_days: int = Field(0, ge=0)
    reason: Optional[str] = None


class PlanResponse(BaseModel):
    """Reading plan response."""
    id: int
    plan_name: str
    deadline: Optional[date] = None
    daily_target_pages: int
    daily_reading_minutes: int
    estimated_hours: Optional[float] = None
    priority_order: Optional[list] = None
    book_ids: Optional[list] = None
    status: str
    confidence: Optional[float] = None
    ai_notes: Optional[str] = None
    schedule_data: Optional[dict] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ── Schedule ─────────────────────────────────────────────────────

class TodayScheduleResponse(BaseModel):
    """GET /api/v1/schedule/today — response."""
    pages: int
    estimated_minutes: int
    book: str
    book_id: int
    chapter: Optional[str] = None
    progress_percentage: float = 0.0

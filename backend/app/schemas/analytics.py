"""
BookPilot AI — Analytics Schemas

Request/response models for analytics and recommendations.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime


# ── Dashboard ────────────────────────────────────────────────────

class DashboardResponse(BaseModel):
    """GET /api/v1/analytics/dashboard — response."""
    total_books: int = 0
    completed_books: int = 0
    in_progress_books: int = 0
    total_pages_read: int = 0
    reading_streak: int = 0
    longest_streak: int = 0
    reading_speed: float = 0.0  # pages per hour
    total_reading_hours: float = 0.0
    avg_pages_per_day: float = 0.0
    goal_completion_percentage: Optional[float] = None


class ReadingSpeedResponse(BaseModel):
    """GET /api/v1/analytics/speed — response."""
    current_speed: float  # pages per hour
    avg_speed_last_7_days: float
    avg_speed_last_30_days: float
    trend: str  # improving, declining, stable


class ReadingStreakResponse(BaseModel):
    """GET /api/v1/analytics/streak — response."""
    current_streak: int
    longest_streak: int
    last_read_date: Optional[date] = None
    total_reading_days: int


class GoalPredictionResponse(BaseModel):
    """GET /api/v1/analytics/prediction — response."""
    predicted_completion_date: Optional[date] = None
    completion_probability: float  # 0.0 - 1.0
    pages_remaining: int
    days_remaining: int
    daily_pages_needed: float
    on_track: bool


# ── Charts ───────────────────────────────────────────────────────

class HeatmapEntry(BaseModel):
    """Single heatmap data point."""
    date: date
    pages: int
    minutes: int


class ChartDataResponse(BaseModel):
    """GET /api/v1/analytics/charts — response."""
    reading_heatmap: list[HeatmapEntry] = []
    weekly_trend: list[dict] = []  # [{week, pages, minutes}]
    genre_distribution: list[dict] = []  # [{genre, count}]
    completion_timeline: list[dict] = []  # [{book, started, completed}]
    daily_pages: list[dict] = []  # [{date, pages}]


# ── Recommendation ───────────────────────────────────────────────

class RecommendationResponse(BaseModel):
    """Recommendation response."""
    id: int
    recommendation_type: str
    book_title: Optional[str] = None
    content: str
    reason: Optional[str] = None
    confidence: float
    generated_at: datetime

    model_config = {"from_attributes": True}


class MoodRecommendationRequest(BaseModel):
    """POST /api/v1/recommendation/mood — request body."""
    mood: str = Field(..., min_length=1, max_length=50, examples=["tired", "energetic", "curious"])

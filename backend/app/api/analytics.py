"""
BookPilot AI — Analytics & Recommendation APIs

Analytics dashboard, streak, charts, and recommendations endpoints.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.database.sqlite import get_db
from app.schemas.analytics import DashboardResponse, RecommendationResponse, MoodRecommendationRequest
from app.schemas.common import StandardResponse
from app.agents.analytics_agent import analytics_agent
from app.agents.recommendation_agent import recommendation_agent

router = APIRouter()

@router.get("/analytics/dashboard", response_model=DashboardResponse)
async def get_dashboard(db: Session = Depends(get_db)):
    """Get analytics dashboard stats."""
    return DashboardResponse(
        total_books=5,
        completed_books=2,
        in_progress_books=3,
        total_pages_read=450,
        reading_streak=12,
        longest_streak=18,
        reading_speed=28.5,
        total_reading_hours=15.8,
        avg_pages_per_day=22.5,
        goal_completion_percentage=75.0,
    )

@router.get("/recommendation")
async def get_recommendation():
    """Get personalized book recommendations."""
    res = recommendation_agent.recommend()
    return StandardResponse(
        data=res["recommendations"],
        timestamp=datetime.now(timezone.utc),
    )

@router.post("/recommendation/mood")
async def get_mood_recommendation(req: MoodRecommendationRequest):
    """Get mood-based book recommendation."""
    res = recommendation_agent.recommend(mood=req.mood)
    return StandardResponse(
        data=res["recommendations"],
        timestamp=datetime.now(timezone.utc),
    )

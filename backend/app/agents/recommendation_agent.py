"""
BookPilot AI — Recommendation Agent

Provides personalized book recommendations and reading order optimization.
"""

from typing import Dict, Any, List
from app.core.logger import get_agent_logger

logger = get_agent_logger("RecommendationAgent")

class RecommendationAgent:
    """Recommendation Agent: Suggests books based on habits and mood."""

    def recommend(self, favorite_genre: str = "Self Help", mood: str = None) -> Dict[str, Any]:
        logger.info(f"RecommendationAgent: Generating recommendations for genre '{favorite_genre}', mood '{mood}'")

        recommendations = [
            {
                "title": "Atomic Habits",
                "author": "James Clear",
                "reason": "Perfect for building consistent reading and learning habits.",
                "confidence": 0.95,
            },
            {
                "title": "Deep Work",
                "author": "Cal Newport",
                "reason": "Great companion for focused reading and cognitive performance.",
                "confidence": 0.90,
            },
            {
                "title": "Make It Stick",
                "author": "Peter C. Brown",
                "reason": "Complements your learning goals with science-backed study techniques.",
                "confidence": 0.88,
            },
        ]

        if mood == "tired":
            recommendations.insert(0, {
                "title": "Show Your Work!",
                "author": "Austin Kleon",
                "reason": "Lightweight, highly visual, and inspiring read when you need a gentle session.",
                "confidence": 0.98,
            })

        return {
            "recommendations": recommendations,
            "confidence": recommendations[0]["confidence"],
        }

recommendation_agent = RecommendationAgent()

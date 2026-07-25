"""
BookPilot AI — Analytics Agent

Calculates reading statistics, streaks, speed, and goal predictions.
"""

from typing import Dict, Any
from app.core.logger import get_agent_logger

logger = get_agent_logger("AnalyticsAgent")

class AnalyticsAgent:
    """Analytics Agent: Provides performance metrics and insights."""

    def process(self, total_pages_read: int, total_minutes: int, streak: int) -> Dict[str, Any]:
        logger.info("AnalyticsAgent: Computing performance statistics")

        hours = total_minutes / 60.0 if total_minutes > 0 else 1.0
        speed = round(total_pages_read / hours, 1) if hours > 0 else 25.0

        return {
            "reading_speed_pph": speed,
            "reading_streak": streak,
            "total_pages_read": total_pages_read,
            "insight": f"Your current reading speed is {speed} pages/hour with a {streak}-day streak!",
        }

analytics_agent = AnalyticsAgent()

"""
BookPilot AI — Calendar MCP Tool Integration

Provides user availability, daily targets, and scheduling capabilities.
"""

from datetime import date, timedelta
from typing import Dict, Any, List
from app.core.logger import get_mcp_logger

logger = get_mcp_logger("CalendarMCP")

class CalendarMCP:
    """Calendar MCP tool for scheduling decisions."""

    def calculate_schedule(
        self,
        total_pages: int,
        deadline: date,
        daily_minutes: int = 30,
        reading_speed_pph: float = 25.0,
    ) -> Dict[str, Any]:
        """Generate a realistic schedule based on availability and deadline."""
        logger.info(f"CalendarMCP: Calculating schedule for {total_pages} pages by {deadline}")

        today = date.today()
        if deadline <= today:
            days_available = 1
        else:
            days_available = (deadline - today).days

        # Pages read per minute
        pages_per_minute = reading_speed_pph / 60.0
        max_daily_pages = int(daily_minutes * pages_per_minute)
        
        required_daily_pages = max(1, int(total_pages / max(1, days_available)))
        
        is_feasible = required_daily_pages <= (max_daily_pages * 1.5)
        
        daily_schedule: List[Dict[str, Any]] = []
        pages_left = total_pages
        current_date = today

        while pages_left > 0 and current_date <= deadline + timedelta(days=30):
            # Weekend bonus: +20% capacity on Saturday/Sunday
            is_weekend = current_date.weekday() in [5, 6]
            day_capacity = int(max_daily_pages * 1.2) if is_weekend else max_daily_pages
            
            pages_today = min(pages_left, day_capacity)
            pages_left -= pages_today
            
            daily_schedule.append({
                "date": current_date.isoformat(),
                "day_name": current_date.strftime("%A"),
                "pages_to_read": pages_today,
                "is_weekend": is_weekend,
                "estimated_minutes": int(pages_today / max(0.1, pages_per_minute)),
            })
            current_date += timedelta(days=1)

        estimated_finish_date = current_date - timedelta(days=1)

        return {
            "is_feasible": is_feasible,
            "days_available": days_available,
            "daily_target_pages": required_daily_pages,
            "estimated_finish_date": estimated_finish_date.isoformat(),
            "schedule": daily_schedule[:30],  # Return up to 30 days
        }

calendar_mcp = CalendarMCP()

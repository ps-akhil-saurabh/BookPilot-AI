"""
BookPilot AI — Scheduling Agent

Generates and adjusts reading schedules using Calendar MCP.
"""

from datetime import date
from typing import Dict, Any, List
from app.mcp.calendar import calendar_mcp
from app.core.logger import get_agent_logger

logger = get_agent_logger("SchedulingAgent")

class SchedulingAgent:
    """Scheduling Agent: Builds realistic adaptive schedules."""

    def process(
        self,
        total_pages: int,
        deadline: date | str,
        daily_minutes: int = 30,
        reading_speed: float = 25.0
    ) -> Dict[str, Any]:
        logger.info(f"SchedulingAgent: Generating schedule for {total_pages} total pages")

        if isinstance(deadline, str):
            deadline = date.fromisoformat(deadline)

        schedule_res = calendar_mcp.calculate_schedule(
            total_pages=total_pages,
            deadline=deadline,
            daily_minutes=daily_minutes,
            reading_speed_pph=reading_speed,
        )

        return {
            "schedule": schedule_res["schedule"],
            "daily_target_pages": schedule_res["daily_target_pages"],
            "is_feasible": schedule_res["is_feasible"],
            "estimated_finish_date": schedule_res["estimated_finish_date"],
            "status": "completed",
        }

scheduling_agent = SchedulingAgent()

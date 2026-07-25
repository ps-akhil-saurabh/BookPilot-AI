"""
BookPilot AI — Reflection Agent

Quality assurance node. Evaluates proposed plans and responses against constraints.
Triggers replanning if feasibility or quality checks fail.
"""

from typing import Dict, Any, List
from app.core.logger import get_agent_logger
from app.core.constants import ReflectionStatus

logger = get_agent_logger("ReflectionAgent")

class ReflectionAgent:
    """Reflection Agent: Validates output before response delivery."""

    def evaluate(self, state: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("ReflectionAgent: Evaluating generated plan and response quality")

        feedback: List[str] = []
        is_approved = True

        # Check scheduling feasibility if present
        sched_output = state.get("scheduling_output")
        if sched_output:
            if not sched_output.get("is_feasible", True):
                is_approved = False
                feedback.append("The requested reading target requires an unsustainable daily reading pace. Consider extending the deadline.")
            
            if sched_output.get("daily_target_pages", 0) > 80:
                is_approved = False
                feedback.append("Daily target exceeds 80 pages per day. Recommend reducing target to prevent reader fatigue.")

        status = ReflectionStatus.APPROVED if is_approved else ReflectionStatus.NEEDS_REVISION
        
        logger.info(f"ReflectionAgent: Decision={status}, FeedbackCount={len(feedback)}")

        return {
            "status": status,
            "approved": is_approved,
            "feedback": feedback,
        }

reflection_agent = ReflectionAgent()

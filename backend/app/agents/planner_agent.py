"""
BookPilot AI — Planner Agent

Central orchestrator. Analyzes user intent, breaks down tasks, and selects required agents.
"""

from typing import Dict, Any, List
from app.core.logger import get_agent_logger
from app.core.constants import IntentType, AgentType

logger = get_agent_logger("PlannerAgent")

class PlannerAgent:
    """Planner Agent: Central intent detection and agent execution planning."""

    def plan_execution(self, user_request: str, intent_override: str = None) -> Dict[str, Any]:
        logger.info(f"PlannerAgent: Analyzing request: '{user_request}'")

        intent = intent_override or self._detect_intent(user_request)
        required_agents = self._select_agents(intent)

        logger.info(f"PlannerAgent: Intent='{intent}', Selected Agents={required_agents}")

        return {
            "intent": intent,
            "selected_agents": required_agents,
        }

    def _detect_intent(self, text: str) -> str:
        text_lower = text.lower()

        if any(w in text_lower for w in ["plan", "schedule", "deadline", "finish books", "target"]):
            return IntentType.READING_PLAN
        elif any(w in text_lower for w in ["explain", "what is", "how does", "meaning of"]):
            return IntentType.EXPLAIN
        elif any(w in text_lower for w in ["summarize", "summary", "overview"]):
            return IntentType.SUMMARIZE
        elif any(w in text_lower for w in ["quiz", "test", "question"]):
            return IntentType.QUIZ
        elif any(w in text_lower for w in ["flashcard", "card", "revision"]):
            return IntentType.FLASHCARD
        elif any(w in text_lower for w in ["vocab", "vocabulary", "word"]):
            return IntentType.VOCABULARY
        elif any(w in text_lower for w in ["recommend", "suggest", "what to read", "mood"]):
            return IntentType.RECOMMENDATION
        elif any(w in text_lower for w in ["stats", "analytics", "progress", "streak", "speed"]):
            return IntentType.ANALYTICS
        elif any(w in text_lower for w in ["missed", "behind", "replan", "catch up"]):
            return IntentType.REPLAN

        return IntentType.GENERAL

    def _select_agents(self, intent: str) -> List[str]:
        mapping = {
            IntentType.READING_PLAN: [AgentType.METADATA, AgentType.SCHEDULING, AgentType.RECOMMENDATION, AgentType.ANALYTICS],
            IntentType.REPLAN: [AgentType.SCHEDULING, AgentType.ANALYTICS],
            IntentType.EXPLAIN: [AgentType.LEARNING],
            IntentType.SUMMARIZE: [AgentType.LEARNING],
            IntentType.QUIZ: [AgentType.LEARNING],
            IntentType.FLASHCARD: [AgentType.LEARNING],
            IntentType.VOCABULARY: [AgentType.LEARNING],
            IntentType.RECOMMENDATION: [AgentType.METADATA, AgentType.RECOMMENDATION],
            IntentType.ANALYTICS: [AgentType.ANALYTICS],
            IntentType.PROGRESS_UPDATE: [AgentType.ANALYTICS, AgentType.SCHEDULING],
            IntentType.GENERAL: [AgentType.LEARNING, AgentType.RECOMMENDATION],
        }
        return mapping.get(intent, [AgentType.LEARNING])

planner_agent = PlannerAgent()

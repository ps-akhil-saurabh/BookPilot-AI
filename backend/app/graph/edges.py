"""
BookPilot AI — LangGraph Edges & Routing Logic

Conditional edge routing for dynamic node execution and reflection loops.
"""

from app.graph.state import BookPilotState
from app.core.constants import ReflectionStatus, AgentType

def route_from_planner(state: BookPilotState) -> str:
    selected = state.get("selected_agents", [])
    if AgentType.METADATA in selected:
        return "metadata"
    elif AgentType.SCHEDULING in selected:
        return "scheduling"
    elif AgentType.LEARNING in selected:
        return "learning"
    elif AgentType.RECOMMENDATION in selected:
        return "recommendation"
    elif AgentType.ANALYTICS in selected:
        return "analytics"
    return "composer"

def route_after_reflection(state: BookPilotState) -> str:
    status = state.get("reflection_status")
    count = state.get("reflection_count", 0)

    if status == ReflectionStatus.NEEDS_REVISION and count < 3:
        return "planner"  # Loop back for replanning
    return "end"

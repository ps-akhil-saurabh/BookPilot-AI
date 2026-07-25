"""
BookPilot AI — LangGraph Router

Maps user requests to graph execution states.
"""

from app.graph.state import BookPilotState
from typing import Dict, Any

def create_initial_state(user_request: str, **kwargs) -> BookPilotState:
    return {
        "user_request": user_request,
        "reflection_count": 0,
        "selected_agents": [],
        **kwargs,
    }

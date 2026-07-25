"""
BookPilot AI — LangGraph Shared State Definition

TypedDict defining the state passed across nodes in the LangGraph execution graph.
"""

from typing import TypedDict, Optional, List, Dict, Any

class BookPilotState(TypedDict, total=False):
    # Input
    user_request: str
    session_id: Optional[str]
    intent: Optional[str]
    book_ids: Optional[List[int]]
    deadline: Optional[str]
    daily_minutes: Optional[int]
    question: Optional[str]
    mood: Optional[str]

    # Agent outputs & Context
    selected_agents: List[str]
    metadata_output: Optional[Dict[str, Any]]
    scheduling_output: Optional[Dict[str, Any]]
    learning_output: Optional[Dict[str, Any]]
    recommendation_output: Optional[Dict[str, Any]]
    analytics_output: Optional[Dict[str, Any]]

    # Response Composition & Reflection
    composed_response: Optional[str]
    reflection_status: Optional[str]  # approved, rejected, needs_revision
    reflection_feedback: Optional[List[str]]
    reflection_count: int

    # Final Output
    final_response: Optional[Dict[str, Any]]
    error: Optional[str]

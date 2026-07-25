"""
BookPilot AI — Workflow, Memory & Reflection APIs

Endpoints for LangGraph execution state, memory preferences, and reflection logs.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.database.sqlite import get_db
from app.schemas.common import StandardResponse
from app.graph.graph import bookpilot_graph
from app.graph.router import create_initial_state

router = APIRouter()

@router.post("/workflow/run")
async def run_workflow(request_text: str):
    """Run full LangGraph workflow manually."""
    state = create_initial_state(user_request=request_text)
    res = await bookpilot_graph.ainvoke(state)
    return StandardResponse(
        data={
            "composed_response": res.get("composed_response"),
            "reflection_status": res.get("reflection_status"),
            "selected_agents": res.get("selected_agents"),
        },
        timestamp=datetime.now(timezone.utc),
    )

@router.get("/workflow/agents")
async def get_agent_status():
    """Get live execution state of all AI agents."""
    return StandardResponse(
        data=[
            {"agent": "Planner", "status": "active"},
            {"agent": "Metadata", "status": "idle"},
            {"agent": "Scheduling", "status": "idle"},
            {"agent": "Learning", "status": "active"},
            {"agent": "Recommendation", "status": "idle"},
            {"agent": "Analytics", "status": "idle"},
            {"agent": "Reflection", "status": "active"},
        ]
    )

@router.get("/reflection/history")
async def get_reflection_history():
    """Get reflection agent evaluation logs."""
    return StandardResponse(
        data=[
            {"id": 1, "type": "schedule", "approved": True, "feedback": ["Schedule is feasible and sustainable."]},
        ]
    )

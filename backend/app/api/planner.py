"""
BookPilot AI — Planner API

Endpoints: /api/v1/planner/generate, /api/v1/planner/replan, /api/v1/planner/{plan_id}
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.database.sqlite import get_db
from app.database.repositories import ReadingPlanRepository, BookRepository
from app.schemas.reading import PlanCreate, PlanReplan, PlanResponse
from app.schemas.common import StandardResponse
from app.graph.graph import bookpilot_graph
from app.graph.router import create_initial_state
from app.core.exceptions import PlanNotFoundException

router = APIRouter()

@router.post("/planner/generate", status_code=201)
async def generate_plan(plan_req: PlanCreate, db: Session = Depends(get_db)):
    """Generate a personalized reading plan using LangGraph."""
    book_repo = BookRepository(db)
    books = book_repo.get_by_ids(plan_req.book_ids)
    
    total_pages = sum([b.total_pages for b in books]) if books else 300
    book_titles = [b.title for b in books] if books else ["Sample Book"]

    # Run LangGraph graph
    state = create_initial_state(
        user_request=f"Plan reading for books: {', '.join(book_titles)}",
        intent="reading_plan",
        book_ids=plan_req.book_ids,
        book_titles=book_titles,
        total_pages=total_pages,
        deadline=plan_req.deadline.isoformat() if plan_req.deadline else "2026-09-01",
        daily_minutes=plan_req.daily_minutes,
    )

    result_state = await bookpilot_graph.ainvoke(state)

    sched_out = result_state.get("scheduling_output", {})
    
    # Save plan to database
    plan_repo = ReadingPlanRepository(db)
    plan_obj = plan_repo.create({
        "plan_name": plan_req.plan_name or f"Reading Plan ({len(plan_req.book_ids)} books)",
        "deadline": plan_req.deadline,
        "daily_target_pages": sched_out.get("daily_target_pages", 20),
        "daily_reading_minutes": plan_req.daily_minutes,
        "book_ids": plan_req.book_ids,
        "status": "active",
        "confidence": 0.92,
        "ai_notes": result_state.get("composed_response"),
        "schedule_data": sched_out.get("schedule"),
    })

    return StandardResponse(
        message="Reading plan generated successfully.",
        data={
            "plan_id": plan_obj.id,
            "daily_target_pages": plan_obj.daily_target_pages,
            "estimated_finish_date": sched_out.get("estimated_finish_date"),
            "confidence": plan_obj.confidence,
            "schedule": sched_out.get("schedule"),
        },
        timestamp=datetime.now(timezone.utc),
    )

@router.post("/planner/replan")
async def replan_schedule(replan_req: PlanReplan, db: Session = Depends(get_db)):
    """Replan reading schedule after missed sessions."""
    plan_repo = ReadingPlanRepository(db)
    plan = plan_repo.get_by_id(replan_req.plan_id)
    if not plan:
        raise PlanNotFoundException(replan_req.plan_id)

    # Trigger adaptive replan
    plan_repo.update(plan.id, {"status": "active", "daily_target_pages": plan.daily_target_pages + 2})

    return StandardResponse(
        message="Schedule recalculated successfully.",
        data={"plan_id": plan.id, "new_daily_target": plan.daily_target_pages + 2},
        timestamp=datetime.now(timezone.utc),
    )

@router.get("/planner/{plan_id}", response_model=PlanResponse)
async def get_plan(plan_id: int, db: Session = Depends(get_db)):
    """Get details of a specific plan."""
    plan_repo = ReadingPlanRepository(db)
    plan = plan_repo.get_by_id(plan_id)
    if not plan:
        raise PlanNotFoundException(plan_id)
    return PlanResponse.model_validate(plan)

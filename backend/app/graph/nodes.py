"""
BookPilot AI — LangGraph Nodes Definition

Graph node handlers that execute specialized agents and update shared state.
"""

from app.graph.state import BookPilotState
from app.agents.planner_agent import planner_agent
from app.agents.metadata_agent import metadata_agent
from app.agents.scheduling_agent import scheduling_agent
from app.agents.learning_agent import learning_agent
from app.agents.recommendation_agent import recommendation_agent
from app.agents.analytics_agent import analytics_agent
from app.agents.reflection_agent import reflection_agent

async def planner_node(state: BookPilotState) -> BookPilotState:
    req = state.get("user_request", "")
    override_intent = state.get("intent")
    res = planner_agent.plan_execution(req, intent_override=override_intent)
    return {
        **state,
        "intent": res["intent"],
        "selected_agents": res["selected_agents"],
    }

async def metadata_node(state: BookPilotState) -> BookPilotState:
    titles = state.get("book_titles", ["Atomic Habits"])
    res = await metadata_agent.process(titles)
    return {**state, "metadata_output": res}

async def scheduling_node(state: BookPilotState) -> BookPilotState:
    total_pages = state.get("total_pages", 300)
    deadline = state.get("deadline", "2026-09-01")
    daily_minutes = state.get("daily_minutes", 30)
    res = scheduling_agent.process(total_pages, deadline, daily_minutes)
    return {**state, "scheduling_output": res}

async def learning_node(state: BookPilotState) -> BookPilotState:
    question = state.get("question") or state.get("user_request")
    book_id = state.get("book_id")
    res = await learning_agent.answer_question(question, book_id=book_id)
    return {**state, "learning_output": res}

async def recommendation_node(state: BookPilotState) -> BookPilotState:
    mood = state.get("mood")
    res = recommendation_agent.recommend(mood=mood)
    return {**state, "recommendation_output": res}

async def analytics_node(state: BookPilotState) -> BookPilotState:
    res = analytics_agent.process(total_pages_read=150, total_minutes=360, streak=12)
    return {**state, "analytics_output": res}

async def response_composer_node(state: BookPilotState) -> BookPilotState:
    intent = state.get("intent")
    if intent == "explain" and state.get("learning_output"):
        response_str = state["learning_output"].get("answer", "")
    elif state.get("scheduling_output"):
        sched = state["scheduling_output"]
        response_str = (
            f"Plan generated! Target: {sched.get('daily_target_pages')} pages/day. "
            f"Estimated finish: {sched.get('estimated_finish_date')}."
        )
    else:
        response_str = "Request processed successfully."

    return {**state, "composed_response": response_str}

async def reflection_node(state: BookPilotState) -> BookPilotState:
    res = reflection_agent.evaluate(state)
    ref_count = state.get("reflection_count", 0) + 1
    return {
        **state,
        "reflection_status": res["status"],
        "reflection_feedback": res["feedback"],
        "reflection_count": ref_count,
    }

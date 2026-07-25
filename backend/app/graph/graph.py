"""
BookPilot AI — LangGraph Graph Builder & Compiler

Assembles and compiles the StateGraph workflow for execution.
"""

from langgraph.graph import StateGraph, START, END
from app.graph.state import BookPilotState
from app.graph.nodes import (
    planner_node,
    metadata_node,
    scheduling_node,
    learning_node,
    recommendation_node,
    analytics_node,
    response_composer_node,
    reflection_node,
)
from app.graph.edges import route_from_planner, route_after_reflection
from app.core.logger import logger

def build_graph():
    """Build and compile the multi-agent orchestration StateGraph."""
    workflow = StateGraph(BookPilotState)

    # Add Nodes
    workflow.add_node("planner", planner_node)
    workflow.add_node("metadata", metadata_node)
    workflow.add_node("scheduling", scheduling_node)
    workflow.add_node("learning", learning_node)
    workflow.add_node("recommendation", recommendation_node)
    workflow.add_node("analytics", analytics_node)
    workflow.add_node("composer", response_composer_node)
    workflow.add_node("reflection", reflection_node)

    # Add Edges
    workflow.add_edge(START, "planner")

    workflow.add_conditional_edges(
        "planner",
        route_from_planner,
        {
            "metadata": "metadata",
            "scheduling": "scheduling",
            "learning": "learning",
            "recommendation": "recommendation",
            "analytics": "analytics",
            "composer": "composer",
        },
    )

    # Next steps after specialized agents to composer
    workflow.add_edge("metadata", "scheduling")
    workflow.add_edge("scheduling", "composer")
    workflow.add_edge("learning", "composer")
    workflow.add_edge("recommendation", "composer")
    workflow.add_edge("analytics", "composer")

    workflow.add_edge("composer", "reflection")

    workflow.add_conditional_edges(
        "reflection",
        route_after_reflection,
        {
            "planner": "planner",
            "end": END,
        },
    )

    compiled_graph = workflow.compile()
    logger.info("LangGraph orchestration graph compiled successfully")
    return compiled_graph

bookpilot_graph = build_graph()

from langgraph.graph import StateGraph, START, END

from app.graph.state import RecruitmentState
from app.graph.agents import (
    resume_agent_node,
    job_description_agent_node,
    skill_gap_agent_node,
)
from app.graph.hr_nodes import final_hr_assessment_node
from app.graph.checkpointer import get_checkpointer


def build_recruitment_graph():
    workflow = StateGraph(RecruitmentState)

    # Add agents
    workflow.add_node(
        "resume_agent",
        resume_agent_node,
    )

    workflow.add_node(
        "job_description_agent",
        job_description_agent_node,
    )

    workflow.add_node(
        "skill_gap_agent",
        skill_gap_agent_node,
    )

    workflow.add_node(
        "hr_assessment",
        final_hr_assessment_node,
    )

    # Workflow sequence
    workflow.add_edge(
        START,
        "resume_agent",
    )

    workflow.add_edge(
        "resume_agent",
        "job_description_agent",
    )

    workflow.add_edge(
        "job_description_agent",
        "skill_gap_agent",
    )

    workflow.add_edge(
        "skill_gap_agent",
        "hr_assessment",
    )

    workflow.add_edge(
        "hr_assessment",
        END,
    )

    return workflow.compile(
        checkpointer=get_checkpointer()
    )


recruitment_graph = build_recruitment_graph()
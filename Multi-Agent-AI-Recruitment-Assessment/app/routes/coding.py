from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.agents.coding_agent import CodingAssessmentAgent
from app.graph.workflow import build_recruitment_graph

router = APIRouter(
    prefix="/coding",
    tags=["Live Coding"],
)


class CodingQuestionRequest(BaseModel):
    candidate_skills: list[str] = Field(default_factory=list)
    missing_skills: list[str] = Field(default_factory=list)


class CodingSubmissionRequest(BaseModel):
    thread_id: str
    code: str = Field(min_length=1)


@router.post("/question")
async def generate_coding_question(
    request: CodingQuestionRequest,
) -> dict[str, Any]:

    agent = CodingAssessmentAgent()

    question = agent.generate_question(
        candidate_skills=request.candidate_skills,
        missing_skills=request.missing_skills,
    )

    return {
        "status": "success",
        "question": question,
    }


@router.post("/submit")
async def submit_coding_solution(
    request: CodingSubmissionRequest,
) -> dict[str, Any]:

    graph = build_recruitment_graph()

    config = {
        "configurable": {
            "thread_id": request.thread_id
        }
    }

    current_state = graph.get_state(config).values

    if not current_state:
        raise HTTPException(
            status_code=404,
            detail="Assessment session not found.",
        )

    coding_questions = current_state.get(
        "coding_questions",
        [],
    )

    if not coding_questions:

        agent = CodingAssessmentAgent()

        question = agent.generate_question(
            candidate_skills=current_state.get(
                "candidate_skills",
                [],
            ),
            missing_skills=current_state.get(
                "missing_skills",
                [],
            ),
        )

        coding_questions = [question]

    coding_submissions = current_state.get(
        "coding_submissions",
        [],
    )

    coding_submissions.append(
        {
            "code": request.code,
        }
    )

    current_state["coding_questions"] = coding_questions
    current_state["coding_submissions"] = coding_submissions

    from app.graph.coding_nodes import (
        execute_coding_submission_node,
    )

    result = execute_coding_submission_node(
        current_state
    )

    current_state.update(result)

    graph.update_state(
        config,
        current_state,
    )

    return {
        "status": "success",
        "stage": current_state.get(
            "current_stage"
        ),
        "coding_score": current_state.get(
            "coding_score",
            0,
        ),
        "evaluation": current_state[
            "coding_submissions"
        ][-1].get("evaluation"),
    }
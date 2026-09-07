from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.graph.workflow import build_recruitment_graph


router = APIRouter(
    prefix="/interview",
    tags=["Adaptive Interview"],
)


class InterviewStartRequest(BaseModel):

    resume_text: str = Field(
        min_length=20,
    )

    job_description_text: str = Field(
        min_length=20,
    )


class InterviewAnswerRequest(BaseModel):

    thread_id: str

    answer: str = Field(
        min_length=1,
    )


@router.post("/start")
async def start_interview(
    request: InterviewStartRequest,
) -> dict[str, Any]:

    graph = build_recruitment_graph()

    thread_id = (
        f"interview-{abs(hash(request.resume_text))}"
    )

    state = {
        "resume_text": request.resume_text,
        "job_description_text": request.job_description_text,
        "errors": [],
    }

    result = graph.invoke(
        state,
        config={
            "configurable": {
                "thread_id": thread_id,
            }
        },
    )

    return {
        "thread_id": thread_id,
        "stage": result.get(
            "current_stage"
        ),
        "candidate_skills": result.get(
            "candidate_skills",
            [],
        ),
        "required_skills": result.get(
            "required_skills",
            [],
        ),
        "matched_skills": result.get(
            "matched_skills",
            [],
        ),
        "missing_skills": result.get(
            "missing_skills",
            [],
        ),
        "skill_match_percentage": result.get(
            "skill_match_percentage",
            0,
        ),
        "message": (
            "Resume and job description processed. "
            "Interview preparation completed."
        ),
    }


@router.post("/answer")
async def submit_answer(
    request: InterviewAnswerRequest,
) -> dict[str, Any]:

    graph = build_recruitment_graph()

    config = {
        "configurable": {
            "thread_id": request.thread_id,
        }
    }

    current_state = graph.get_state(
        config
    ).values

    if not current_state:
        raise HTTPException(
            status_code=404,
            detail="Interview session not found.",
        )

    questions = current_state.get(
        "interview_questions",
        [],
    )

    answers = current_state.get(
        "interview_answers",
        [],
    )

    if questions:
        answers = answers + [
            {
                "answer": request.answer,
            }
        ]

    current_state["interview_answers"] = answers

    result = graph.invoke(
        current_state,
        config=config,
    )

    return {
        "thread_id": request.thread_id,
        "stage": result.get(
            "current_stage"
        ),
        "interview_questions": result.get(
            "interview_questions",
            [],
        ),
        "interview_score": result.get(
            "interview_score",
            0,
        ),
        "technical_score": result.get(
            "technical_score",
            0,
        ),
        "recommendation": result.get(
            "recommendation",
        ),
    }
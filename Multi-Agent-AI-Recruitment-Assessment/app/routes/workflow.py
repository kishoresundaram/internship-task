from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.graph.workflow import build_recruitment_graph


router = APIRouter(
    prefix="/workflow",
    tags=["Recruitment Workflow"],
)


class WorkflowRequest(BaseModel):
    candidate_id: int = 0
    job_description_id: int = 0

    resume_text: str = Field(
        ...,
        min_length=20,
    )

    job_description_text: str = Field(
        ...,
        min_length=20,
    )

    technical: float = Field(
        default=0,
        ge=0,
        le=100,
    )

    interview: float = Field(
        default=0,
        ge=0,
        le=100,
    )

    coding: float = Field(
        default=0,
        ge=0,
        le=100,
    )

    communication: float = Field(
        default=0,
        ge=0,
        le=100,
    )

    star: float = Field(
        default=0,
        ge=0,
        le=100,
    )

    protocol: float = Field(
        default=0,
        ge=0,
        le=100,
    )


@router.post("/run")
async def run_recruitment_workflow(
    request: WorkflowRequest,
) -> dict[str, Any]:

    graph = build_recruitment_graph()

    thread_id = (
        f"recruitment-"
        f"{request.candidate_id}-"
        f"{request.job_description_id}"
    )

    initial_state = {
        "candidate_id": request.candidate_id,
        "job_description_id": request.job_description_id,

        "resume_text": request.resume_text,
        "job_description_text": request.job_description_text,

        "technical_score": request.technical,
        "interview_score": request.interview,
        "coding_score": request.coding,
        "communication_score": request.communication,
        "star_score": request.star,
        "protocol_score": request.protocol,

        "errors": [],
    }

    result = graph.invoke(
        initial_state,
        config={
            "configurable": {
                "thread_id": thread_id,
            }
        },
    )

    return {
        "status": "success",
        "thread_id": thread_id,

        "workflow_stage": result.get(
            "current_stage"
        ),

        "candidate_id": result.get(
            "candidate_id"
        ),

        "job_description_id": result.get(
            "job_description_id"
        ),

        "resume_profile": result.get(
            "resume_profile",
            {},
        ),

        "job_description_profile": result.get(
            "job_description_profile",
            {},
        ),

        "skill_analysis": {
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

            "additional_skills": result.get(
                "additional_skills",
                [],
            ),

            "match_percentage": result.get(
                "skill_match_percentage",
                0,
            ),
        },

        "assessment": {
            "technical": result.get(
                "technical_score",
                0,
            ),

            "interview": result.get(
                "interview_score",
                0,
            ),

            "coding": result.get(
                "coding_score",
                0,
            ),

            "communication": result.get(
                "communication_score",
                0,
            ),

            "star": result.get(
                "star_score",
                0,
            ),

            "protocol": result.get(
                "protocol_score",
                0,
            ),

            "overall_score": result.get(
                "overall_score",
                0,
            ),
        },

        "recommendation": result.get(
            "recommendation"
        ),

        "shortlisted": result.get(
            "shortlisted",
            False,
        ),

        "hr_decision": result.get(
            "hr_decision"
        ),

        "hr_reason": result.get(
            "hr_reason"
        ),

        "human_review_required": result.get(
            "human_review_required",
            False,
        ),

        "errors": result.get(
            "errors",
            [],
        ),
    }
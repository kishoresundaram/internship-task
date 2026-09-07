from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.agents.hr_agent import HRAssessmentAgent


router = APIRouter(
    prefix="/hr",
    tags=["HR Shortlisting"],
)


class HRAssessmentRequest(BaseModel):

    candidate_id: int = 0

    candidate_profile: dict[str, Any] = Field(
        default_factory=dict
    )

    skill_match: float = 0
    technical: float = 0
    interview: float = 0
    coding: float = 0
    communication: float = 0
    star: float = 0
    protocol: float = 0


@router.post("/assess")
async def assess_candidate(
    request: HRAssessmentRequest,
) -> dict[str, Any]:

    candidate = {
        "id": request.candidate_id,
        "structured_profile": (
            request.candidate_profile
        ),
        "skills": request.candidate_profile.get(
            "skills",
            [],
        ),
        "experience": request.candidate_profile.get(
            "experience",
            [],
        ),
        "education": request.candidate_profile.get(
            "education",
            [],
        ),
    }

    agent = HRAssessmentAgent()

    result = agent.assess(
        candidate=candidate,
        skill_match=request.skill_match,
        technical=request.technical,
        interview=request.interview,
        coding=request.coding,
        communication=request.communication,
        star=request.star,
        protocol=request.protocol,
    )

    return {
        "status": "success",
        **result,
    }


@router.post("/shortlist")
async def shortlist_candidate(
    request: HRAssessmentRequest,
) -> dict[str, Any]:

    candidate = {
        "id": request.candidate_id,
        "structured_profile": (
            request.candidate_profile
        ),
        "skills": request.candidate_profile.get(
            "skills",
            [],
        ),
    }

    agent = HRAssessmentAgent()

    result = agent.assess(
        candidate=candidate,
        skill_match=request.skill_match,
        technical=request.technical,
        interview=request.interview,
        coding=request.coding,
        communication=request.communication,
        star=request.star,
        protocol=request.protocol,
    )

    return {
        "status": "success",
        "candidate_id": request.candidate_id,
        "shortlisted": (
            result["hr_decision"]
            == "shortlist"
        ),
        "overall_score": result[
            "merit_assessment"
        ]["overall_score"],
        "recommendation": result[
            "merit_assessment"
        ]["recommendation"],
        "hr_decision": result[
            "hr_decision"
        ],
        "hr_reason": result[
            "hr_reason"
        ],
    }
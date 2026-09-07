from typing import Any

from app.agents.hr_agent import HRAssessmentAgent


def final_hr_assessment_node(
    state: dict[str, Any],
) -> dict[str, Any]:

    candidate = {
        "id": state.get(
            "candidate_id",
            "UNKNOWN",
        ),
        "structured_profile": state.get(
            "resume_profile",
            {},
        ),
        "skills": state.get(
            "candidate_skills",
            [],
        ),
    }

    skill_match = state.get(
        "skill_match_percentage",
        0,
    )

    technical = state.get(
        "technical_score",
        0,
    )

    interview = state.get(
        "interview_score",
        0,
    )

    coding = state.get(
        "coding_score",
        0,
    )

    communication = state.get(
        "communication_score",
        0,
    )

    star = state.get(
        "star_score",
        0,
    )

    protocol = state.get(
        "protocol_score",
        0,
    )

    agent = HRAssessmentAgent()

    result = agent.assess(
        candidate=candidate,
        skill_match=skill_match,
        technical=technical,
        interview=interview,
        coding=coding,
        communication=communication,
        star=star,
        protocol=protocol,
    )

    return {
        "overall_score": result[
            "merit_assessment"
        ]["overall_score"],
        "recommendation": result[
            "merit_assessment"
        ]["recommendation"],
        "shortlisted": (
            result["hr_decision"]
            == "shortlist"
        ),
        "hr_decision": result[
            "hr_decision"
        ],
        "hr_reason": result[
            "hr_reason"
        ],
        "hr_assessment": result,
        "human_review_required": (
            result["hr_decision"]
            == "review"
        ),
        "current_stage": "hr_assessment_completed",
    }
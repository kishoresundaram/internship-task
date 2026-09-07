from typing import Any

from app.agents.job_description_agent import (
    JobDescriptionProcessingAgent,
)
from app.agents.resume_agent import (
    ResumeProcessingAgent,
)
from app.services.semantic_skill_gap_service import (
    SemanticSkillGapService,
)


def resume_agent_node(
    state: dict[str, Any],
) -> dict[str, Any]:

    resume_text = state.get(
        "resume_text",
        "",
    )

    if not resume_text:
        return {
            "errors": ["Resume text is missing"],
            "current_stage": "resume_error",
        }

    agent = ResumeProcessingAgent()

    profile = agent.process(resume_text)

    profile_data = profile.to_dict()

    return {
        "resume_profile": profile_data,
        "candidate_skills": profile_data.get(
            "skills",
            [],
        ),
        "current_stage": "resume_processed",
    }


def job_description_agent_node(
    state: dict[str, Any],
) -> dict[str, Any]:

    job_description_text = state.get(
        "job_description_text",
        "",
    )

    if not job_description_text:
        return {
            "errors": [
                "Job description text is missing"
            ],
            "current_stage": "jd_error",
        }

    agent = JobDescriptionProcessingAgent()

    profile = agent.process(
        job_description_text
    )

    profile_data = profile.to_dict()

    required_skills = profile_data.get(
        "required_skills",
        [],
    )

    if isinstance(required_skills, str):
        required_skills = [
            skill.strip()
            for skill in required_skills.split(",")
            if skill.strip()
        ]

    return {
        "job_description_profile": profile_data,
        "required_skills": required_skills,
        "current_stage": "jd_processed",
    }


def skill_gap_agent_node(
    state: dict[str, Any],
) -> dict[str, Any]:

    candidate_skills = state.get(
        "candidate_skills",
        [],
    )

    required_skills = state.get(
        "required_skills",
        [],
    )

    if not candidate_skills:
        return {
            "errors": [
                "Candidate skills are missing"
            ],
            "current_stage": "skill_gap_error",
        }

    if not required_skills:
        return {
            "errors": [
                "Required skills are missing"
            ],
            "current_stage": "skill_gap_error",
        }

    service = SemanticSkillGapService()

    result = service.analyze(
        candidate_skills=candidate_skills,
        required_skills=required_skills,
    )

    return {
        "matched_skills": result[
            "matched_skills"
        ],
        "missing_skills": result[
            "missing_skills"
        ],
        "additional_skills": result[
            "additional_skills"
        ],
        "skill_match_percentage": result[
            "match_percentage"
        ],
        "current_stage": "skill_gap_completed",
    }
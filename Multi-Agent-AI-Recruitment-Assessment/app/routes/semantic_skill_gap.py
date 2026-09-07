from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.models.candidate import Candidate
from app.models.job_description import JobDescription
from app.services.semantic_skill_gap_service import (
    SemanticSkillGapService,
)

router = APIRouter(
    prefix="/semantic-skill-gap",
    tags=["Semantic Skill Gap"],
)


@router.get("/{candidate_id}/{job_description_id}")
async def semantic_skill_gap(
    candidate_id: int,
    job_description_id: int,
    db: AsyncSession = Depends(get_db),
):
    candidate_result = await db.execute(
        select(Candidate).where(
            Candidate.id == candidate_id
        )
    )

    candidate = candidate_result.scalar_one_or_none()

    if candidate is None:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found",
        )

    job_result = await db.execute(
        select(JobDescription).where(
            JobDescription.id == job_description_id
        )
    )

    job_description = job_result.scalar_one_or_none()

    if job_description is None:
        raise HTTPException(
            status_code=404,
            detail="Job description not found",
        )

    candidate_profile = (
        candidate.structured_profile or {}
    )

    candidate_skills = candidate_profile.get(
        "skills",
        [],
    )

    if isinstance(candidate_skills, dict):
        candidate_skills = list(
            candidate_skills.keys()
        )

    required_skills = []

    if job_description.required_skills:
        required_skills = [
            skill.strip()
            for skill in job_description.required_skills.split(",")
            if skill.strip()
        ]

    if not candidate_skills:
        raise HTTPException(
            status_code=400,
            detail="Candidate has no structured skills",
        )

    if not required_skills:
        raise HTTPException(
            status_code=400,
            detail="Job description has no required skills",
        )

    service = SemanticSkillGapService()

    result = service.analyze(
        candidate_skills=candidate_skills,
        required_skills=required_skills,
    )

    return {
        "candidate_id": candidate_id,
        "job_description_id": job_description_id,
        "candidate_skills": candidate_skills,
        "required_skills": required_skills,
        "analysis": result,
    }
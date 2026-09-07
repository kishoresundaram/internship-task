from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.models.candidate import Candidate
from app.models.job_description import JobDescription
from app.services.skill_gap_service import (
    SkillGapService,
    SkillGapProcessingError,
    SkillGapValidationError,
)


router = APIRouter(
    prefix="/skill-gap",
    tags=["Skill Gap Analysis"],
)


skill_gap_service = SkillGapService()


@router.get(
    "/{candidate_id}/{job_description_id}"
)
async def analyze_skill_gap(
    candidate_id: int,
    job_description_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Compare a candidate's skills against
    the required and preferred skills
    of a job description.
    """

    candidate_result = await db.execute(
        select(Candidate).where(
            Candidate.id == candidate_id
        )
    )

    candidate = (
        candidate_result.scalar_one_or_none()
    )

    if candidate is None:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found",
        )

    job_result = await db.execute(
        select(JobDescription).where(
            JobDescription.id
            == job_description_id
        )
    )

    job_description = (
        job_result.scalar_one_or_none()
    )

    if job_description is None:
        raise HTTPException(
            status_code=404,
            detail="Job description not found",
        )

    candidate_profile = (
        candidate.structured_profile
        or {}
    )

    candidate_skills = (
        candidate_profile.get(
            "skills",
            []
        )
    )

    required_skills = []

    if job_description.required_skills:

        required_skills = [
            skill.strip()
            for skill in (
                job_description
                .required_skills
                .split(",")
            )
            if skill.strip()
        ]

    preferred_skills = (
        job_description.preferred_skills
        or []
    )

    try:

        result = skill_gap_service.analyze(
            candidate_skills=candidate_skills,
            required_skills=required_skills,
            preferred_skills=preferred_skills,
        )

    except SkillGapValidationError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except SkillGapProcessingError as exc:

        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc

    return {
        "candidate_id": candidate_id,
        "job_description_id": job_description_id,
        "candidate_name": candidate.name,
        "job_title": job_description.job_title,
        "analysis": result.to_dict(),
    }
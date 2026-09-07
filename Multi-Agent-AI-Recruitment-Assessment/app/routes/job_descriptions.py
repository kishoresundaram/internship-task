from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.models.job_description import JobDescription
from app.schemas.job_description import (
    JobDescriptionCreate,
    JobDescriptionResponse,
)
from app.services.job_description_service import (
    JobDescriptionProcessingError,
    JobDescriptionService,
    JobDescriptionValidationError,
)


router = APIRouter(
    prefix="/job-descriptions",
    tags=["Job Descriptions"],
)


job_description_service = (
    JobDescriptionService()
)


@router.post(
    "/",
    response_model=JobDescriptionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_job_description(
    job_data: JobDescriptionCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Create and process a job description.
    """

    try:
        profile = (
            job_description_service
            .process_job_description(
                job_data.description
            )
        )

    except JobDescriptionValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    except JobDescriptionProcessingError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc

    structured_profile = (
        profile.to_dict()
    )

    job_description = JobDescription(
        job_title=(
            job_data.job_title
            or profile.job_title
            or "Unknown Job"
        ),
        company=(
            job_data.company
            or profile.company
        ),
        description=profile.raw_text,
        required_skills=", ".join(
            profile.required_skills
        ),
        preferred_skills=(
            profile.preferred_skills
        ),
        experience_required=(
            job_data.experience_required
            or profile.experience_required
        ),
        education_required=(
            profile.education_required
        ),
        responsibilities=(
            profile.responsibilities
        ),
        qualifications=(
            profile.qualifications
        ),
        location=(
            job_data.location
            or profile.location
        ),
        employment_type=(
            profile.employment_type
        ),
        structured_profile=(
            structured_profile
        ),
    )

    db.add(job_description)

    await db.commit()

    await db.refresh(job_description)

    return job_description


@router.get(
    "/",
    response_model=list[JobDescriptionResponse],
)
async def get_job_descriptions(
    db: AsyncSession = Depends(get_db),
):
    """
    Get all job descriptions.
    """

    result = await db.execute(
        select(JobDescription)
        .order_by(JobDescription.id)
    )

    return result.scalars().all()


@router.get(
    "/{job_description_id}",
    response_model=JobDescriptionResponse,
)
async def get_job_description(
    job_description_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Get a single job description.
    """

    result = await db.execute(
        select(JobDescription).where(
            JobDescription.id
            == job_description_id
        )
    )

    job_description = (
        result.scalar_one_or_none()
    )

    if job_description is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job description not found",
        )

    return job_description


@router.delete(
    "/{job_description_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_job_description(
    job_description_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Delete a job description.
    """

    result = await db.execute(
        select(JobDescription).where(
            JobDescription.id
            == job_description_id
        )
    )

    job_description = (
        result.scalar_one_or_none()
    )

    if job_description is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job description not found",
        )

    await db.delete(job_description)

    await db.commit()
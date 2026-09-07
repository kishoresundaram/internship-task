from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.models.assessments import Assessment
from app.models.candidate import Candidate
from app.models.job_description import JobDescription
from app.schemas.assessment import (
    AssessmentCreate,
    AssessmentResponse,
    AssessmentUpdate,
)

router = APIRouter(
    prefix="/assessments",
    tags=["Assessments"],
)


@router.post(
    "/",
    response_model=AssessmentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_assessment(
    assessment_data: AssessmentCreate,
    db: AsyncSession = Depends(get_db),
):
    candidate_result = await db.execute(
        select(Candidate).where(
            Candidate.id == assessment_data.candidate_id
        )
    )

    candidate = candidate_result.scalar_one_or_none()

    if candidate is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found",
        )

    job_result = await db.execute(
        select(JobDescription).where(
            JobDescription.id == assessment_data.job_description_id
        )
    )

    job_description = job_result.scalar_one_or_none()

    if job_description is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job description not found",
        )

    assessment = Assessment(
        candidate_id=assessment_data.candidate_id,
        job_description_id=assessment_data.job_description_id,
        status="pending",
    )

    db.add(assessment)
    await db.commit()
    await db.refresh(assessment)

    return assessment


@router.get(
    "/",
    response_model=list[AssessmentResponse],
)
async def get_assessments(
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Assessment).order_by(Assessment.id)
    )

    return result.scalars().all()


@router.get(
    "/{assessment_id}",
    response_model=AssessmentResponse,
)
async def get_assessment(
    assessment_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Assessment).where(
            Assessment.id == assessment_id
        )
    )

    assessment = result.scalar_one_or_none()

    if assessment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found",
        )

    return assessment


@router.patch(
    "/{assessment_id}",
    response_model=AssessmentResponse,
)
async def update_assessment(
    assessment_id: int,
    assessment_data: AssessmentUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Assessment).where(
            Assessment.id == assessment_id
        )
    )

    assessment = result.scalar_one_or_none()

    if assessment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found",
        )

    update_data = assessment_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(assessment, field, value)

    await db.commit()
    await db.refresh(assessment)

    return assessment


@router.delete(
    "/{assessment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_assessment(
    assessment_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Assessment).where(
            Assessment.id == assessment_id
        )
    )

    assessment = result.scalar_one_or_none()

    if assessment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found",
        )

    await db.delete(assessment)
    await db.commit()
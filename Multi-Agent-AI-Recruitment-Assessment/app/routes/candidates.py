from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.models.candidate import Candidate
from app.schemas.candidate import CandidateCreate, CandidateResponse

router = APIRouter(
    prefix="/candidates",
    tags=["Candidates"],
)


@router.post(
    "/",
    response_model=CandidateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_candidate(
    candidate_data: CandidateCreate,
    db: AsyncSession = Depends(get_db),
):
    existing_candidate = await db.execute(
        select(Candidate).where(Candidate.email == candidate_data.email)
    )

    if existing_candidate.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Candidate with this email already exists",
        )

    candidate = Candidate(
        name=candidate_data.name,
        email=candidate_data.email,
        phone=candidate_data.phone,
        resume_text=candidate_data.resume_text,
    )

    db.add(candidate)
    await db.commit()
    await db.refresh(candidate)

    return candidate


@router.get(
    "/",
    response_model=list[CandidateResponse],
)
async def get_candidates(
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Candidate).order_by(Candidate.id)
    )

    return result.scalars().all()


@router.get(
    "/{candidate_id}",
    response_model=CandidateResponse,
)
async def get_candidate(
    candidate_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Candidate).where(Candidate.id == candidate_id)
    )

    candidate = result.scalar_one_or_none()

    if candidate is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found",
        )

    return candidate


@router.delete(
    "/{candidate_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_candidate(
    candidate_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Candidate).where(Candidate.id == candidate_id)
    )

    candidate = result.scalar_one_or_none()

    if candidate is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found",
        )

    await db.delete(candidate)
    await db.commit()
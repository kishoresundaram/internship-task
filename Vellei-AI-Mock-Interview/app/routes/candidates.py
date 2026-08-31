from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models.candidate import Candidate
from app.schemas.candidate import CandidateCreate, CandidateResponse

router = APIRouter(
    prefix="/candidates",
    tags=["Candidates"]
)


@router.post("/", response_model=CandidateResponse)
def create_candidate(
    candidate_data: CandidateCreate,
    db: Session = Depends(get_db)
):
    # Check if email already exists
    existing_candidate = db.query(Candidate).filter(
        Candidate.email == candidate_data.email
    ).first()

    if existing_candidate:
        raise HTTPException(
            status_code=400,
            detail="A candidate with this email already exists."
        )

    candidate = Candidate(
        name=candidate_data.name,
        email=candidate_data.email,
        phone=candidate_data.phone,
        resume_text=candidate_data.resume_text
    )

    try:
        db.add(candidate)
        db.commit()
        db.refresh(candidate)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="A candidate with this email already exists."
        )

    return candidate


@router.get("/", response_model=list[CandidateResponse])
def get_candidates(
    db: Session = Depends(get_db)
):
    return db.query(Candidate).all()


@router.get("/{candidate_id}", response_model=CandidateResponse)
def get_candidate(
    candidate_id: int,
    db: Session = Depends(get_db)
):
    candidate = db.query(Candidate).filter(
        Candidate.id == candidate_id
    ).first()

    if not candidate:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found"
        )

    return candidate
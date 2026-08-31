from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.candidate import Candidate
from app.models.interview import InterviewSession
from app.models.question import Question


router = APIRouter(
    prefix="/interview",
    tags=["Interview"]
)


class InterviewStartRequest(BaseModel):
    candidate_id: int
    job_title: str
    difficulty: str = "medium"


@router.post("/start")
def start_interview(
    data: InterviewStartRequest,
    db: Session = Depends(get_db)
):

    # -----------------------------
    # Find Candidate
    # -----------------------------

    candidate = (
        db.query(Candidate)
        .filter(Candidate.id == data.candidate_id)
        .first()
    )

    if not candidate:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found"
        )


    # -----------------------------
    # Create Interview Session
    # -----------------------------

    interview = InterviewSession(
        candidate_id=data.candidate_id,
        job_title=data.job_title,
        difficulty=data.difficulty,
        status="started"
    )

    db.add(interview)
    db.commit()
    db.refresh(interview)


    # -----------------------------
    # Create First Question
    # -----------------------------

    question_text = (
        f"Tell me about your experience with "
        f"the skills required for the {data.job_title} role."
    )

    question = Question(
        session_id=interview.id,
        question_text=question_text,
        difficulty=data.difficulty,
        question_type="technical"
    )

    db.add(question)
    db.commit()
    db.refresh(question)


    # -----------------------------
    # Response
    # -----------------------------

    return {
        "success": True,
        "interview_id": interview.id,
        "candidate_id": data.candidate_id,
        "job_title": data.job_title,
        "difficulty": data.difficulty,
        "question_id": question.id,
        "question": question.question_text
    }
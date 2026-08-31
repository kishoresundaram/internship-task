from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.candidate import Candidate
from app.models.interview import Interview
from app.models.evaluation import Evaluation


router = APIRouter(
    prefix="/report",
    tags=["Report"]
)


@router.get("/{candidate_id}")
def get_candidate_report(
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

    interviews = db.query(Interview).filter(
        Interview.candidate_id == candidate_id
    ).all()

    evaluations = []

    for interview in interviews:
        interview_evaluations = db.query(Evaluation).filter(
            Evaluation.interview_id == interview.id
        ).all()

        for evaluation in interview_evaluations:
            evaluations.append(evaluation)

    if not evaluations:
        return {
            "success": True,
            "candidate_id": candidate.id,
            "candidate_name": candidate.name,
            "total_questions": 0,
            "average_score": 0,
            "evaluations": [],
            "message": "No evaluations available yet"
        }

    total_score = sum(
        evaluation.score for evaluation in evaluations
    )

    average_score = round(
        total_score / len(evaluations),
        2
    )

    return {
        "success": True,
        "candidate_id": candidate.id,
        "candidate_name": candidate.name,
        "total_questions": len(evaluations),
        "average_score": average_score,
        "evaluations": [
            {
                "evaluation_id": evaluation.id,
                "question": evaluation.question,
                "answer": evaluation.answer,
                "score": evaluation.score,
                "feedback": evaluation.feedback,
                "strengths": evaluation.strengths,
                "improvements": evaluation.improvements
            }
            for evaluation in evaluations
        ]
    }
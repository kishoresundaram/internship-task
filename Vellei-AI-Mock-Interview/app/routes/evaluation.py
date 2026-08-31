from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.interview import Interview
from app.models.question import Question
from app.models.answer import Answer
from app.models.evaluation import Evaluation
from app.services.gemini_service import generate_evaluation


router = APIRouter(
    prefix="/evaluation",
    tags=["Evaluation"]
)


class EvaluationRequest(BaseModel):
    interview_id: int
    question: str
    answer: str


@router.post("/")
def evaluate_answer(
    data: EvaluationRequest,
    db: Session = Depends(get_db)
):

    # -----------------------------
    # Find Interview
    # -----------------------------

    interview = (
        db.query(Interview)
        .filter(Interview.id == data.interview_id)
        .first()
    )

    if not interview:
        raise HTTPException(
            status_code=404,
            detail="Interview not found"
        )


    # -----------------------------
    # Find Question
    # -----------------------------

    question = (
        db.query(Question)
        .filter(
            Question.session_id == interview.id,
            Question.question_text == data.question
        )
        .first()
    )

    # If exact question is not found,
    # use the latest question from this interview.

    if not question:

        question = (
            db.query(Question)
            .filter(
                Question.session_id == interview.id
            )
            .order_by(Question.id.desc())
            .first()
        )

    if not question:
        raise HTTPException(
            status_code=404,
            detail="Question not found for this interview"
        )


    # -----------------------------
    # Generate AI Evaluation
    # -----------------------------

    try:

        result = generate_evaluation(
            question=data.question,
            answer=data.answer
        )


        # -----------------------------
        # Create Answer
        # -----------------------------

        new_answer = Answer(
            question_id=question.id,
            answer_text=data.answer,
            score=result.get("score", 0)
        )

        db.add(new_answer)
        db.commit()
        db.refresh(new_answer)


        # -----------------------------
        # Create Evaluation
        # -----------------------------

        evaluation = Evaluation(
            answer_id=new_answer.id,
            score=result.get("score", 0),
            technical_score=result.get(
                "technical_score",
                result.get("score", 0)
            ),
            communication_score=result.get(
                "communication_score",
                result.get("score", 0)
            ),
            relevance_score=result.get(
                "relevance_score",
                result.get("score", 0)
            ),
            feedback=result.get(
                "feedback",
                ""
            )
        )

        db.add(evaluation)
        db.commit()
        db.refresh(evaluation)


        # -----------------------------
        # Response
        # -----------------------------

        return {
            "success": True,
            "evaluation_id": evaluation.id,
            "answer_id": new_answer.id,
            "question_id": question.id,
            "score": evaluation.score,
            "feedback": evaluation.feedback,
            "strengths": result.get(
                "strengths",
                ""
            ),
            "improvements": result.get(
                "improvements",
                ""
            )
        }


    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
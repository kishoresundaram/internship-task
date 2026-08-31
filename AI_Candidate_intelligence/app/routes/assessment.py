from fastapi import APIRouter, HTTPException

from app.services.assessment_service import (
    generate_assessment,
    evaluate_answers
)


router = APIRouter(
    prefix="/assessment",
    tags=["Assessment"]
)


@router.post("/generate")
async def generate(data: dict):

    role = data.get("role")

    if not role:
        raise HTTPException(
            status_code=400,
            detail="role is required"
        )

    questions = generate_assessment(role)

    if not questions:
        raise HTTPException(
            status_code=404,
            detail="Role not supported"
        )

    return {
        "role": role,
        "question_count": len(questions),
        "questions": questions
    }


@router.post("/evaluate")
async def evaluate(data: dict):

    role = data.get("role")
    answers = data.get("answers")

    if not role:
        raise HTTPException(
            status_code=400,
            detail="role is required"
        )

    if not answers:
        raise HTTPException(
            status_code=400,
            detail="answers are required"
        )

    result = evaluate_answers(role, answers)

    return {
        "role": role,
        **result
    }
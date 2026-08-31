from fastapi import APIRouter, HTTPException

from app.services.gap_service import (
    detect_gaps,
    generate_gap_questions
)


router = APIRouter(
    prefix="/gaps",
    tags=["Gap Detection"]
)


@router.post("/analyze")
async def analyze_gaps(data: dict):

    profile = data.get("profile")

    if not profile:
        raise HTTPException(
            status_code=400,
            detail="profile is required"
        )

    gaps = detect_gaps(profile)

    questions = generate_gap_questions(gaps)

    return {
        "gaps_detected": gaps,
        "gap_count": len(gaps),
        "questions": questions
    }
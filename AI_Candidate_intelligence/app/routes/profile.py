from fastapi import APIRouter, HTTPException

from app.services.profile_service import (
    extract_profile,
    calculate_completeness
)


router = APIRouter(
    prefix="/profile",
    tags=["Candidate Profile"]
)


@router.post("/analyze")
async def analyze_profile(data: dict):

    resume_text = data.get("resume_text")

    if not resume_text:
        raise HTTPException(
            status_code=400,
            detail="resume_text is required"
        )

    profile = extract_profile(resume_text)

    completeness, missing = calculate_completeness(profile)

    return {
        "profile": profile,
        "completeness_score": completeness,
        "missing_information": missing
    }
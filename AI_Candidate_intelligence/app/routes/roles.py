from fastapi import APIRouter, HTTPException

from app.services.role_service import recommend_roles


router = APIRouter(
    prefix="/roles",
    tags=["Role Recommendation"]
)


@router.post("/recommend")
async def recommend(data: dict):

    skills = data.get("skills")

    if not skills:
        raise HTTPException(
            status_code=400,
            detail="skills are required"
        )

    recommendations = recommend_roles(skills)

    return {
        "candidate_skills": skills,
        "recommended_roles": recommendations
    }
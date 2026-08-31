from fastapi import FastAPI

from app.routes.resume import router as resume_router
from app.routes.profile import router as profile_router
from app.routes.gaps import router as gaps_router
from app.routes.roles import router as roles_router
from app.routes.assessment import router as assessment_router


app = FastAPI(
    title="AI Candidate Intelligence",
    description="AI-powered candidate profiling and role readiness platform",
    version="1.0.0"
)


app.include_router(resume_router)
app.include_router(profile_router)
app.include_router(gaps_router)
app.include_router(roles_router)
app.include_router(assessment_router)


@app.get("/")
def home():
    return {
        "message": "AI Candidate Intelligence API is running",
        "status": "success"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
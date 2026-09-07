from fastapi import FastAPI

from app.routes.assessments import router as assessments_router
from app.routes.candidates import router as candidates_router
from app.routes.coding import router as coding_router
from app.routes.final_assessment import router as final_assessment_router
from app.routes.hr import router as hr_router
from app.routes.interview import router as interview_router
from app.routes.job_descriptions import router as job_descriptions_router
from app.routes.resume import router as resume_router
from app.routes.screening import router as screening_router
from app.routes.semantic_skill_gap import router as semantic_skill_gap_router
from app.routes.skill_gap import router as skill_gap_router
from app.routes.tasks import router as tasks_router
from app.routes.workflow import router as workflow_router


app = FastAPI(
    title="Multi-Agent AI Recruitment Assessment",
    description="AI-driven multi-agent recruitment assessment platform",
    version="1.0.0",
)


app.include_router(candidates_router)
app.include_router(job_descriptions_router)
app.include_router(assessments_router)
app.include_router(resume_router)
app.include_router(skill_gap_router)
app.include_router(semantic_skill_gap_router)
app.include_router(interview_router)
app.include_router(coding_router)
app.include_router(screening_router)
app.include_router(hr_router)
app.include_router(tasks_router)
app.include_router(final_assessment_router)
app.include_router(workflow_router)


@app.get("/")
async def root():
    return {
        "message": "Multi-Agent AI Recruitment Assessment API is running"
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy"
    }
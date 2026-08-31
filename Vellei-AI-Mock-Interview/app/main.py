from fastapi import FastAPI

from app.database import create_tables

from app.routes.candidates import router as candidate_router
from app.routes.interview import router as interview_router
from app.routes.evaluation import router as evaluation_router
from app.routes.report import router as report_router


app = FastAPI(
    title="Vellei AI Mock Interview",
    description="AI-powered mock interview system using FastAPI, SQLite and Gemini",
    version="1.0.0"
)


# Create database tables
create_tables()


# Register API routes
app.include_router(candidate_router)
app.include_router(interview_router)
app.include_router(evaluation_router)
app.include_router(report_router)


@app.get("/")
def root():
    return {
        "success": True,
        "message": "Vellei AI Mock Interview API is running"
    }


@app.get("/health")
def health_check():
    return {
        "success": True,
        "status": "healthy"
    }
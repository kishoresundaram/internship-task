from fastapi import FastAPI
from sqlalchemy import text

from app.db.database import Base, engine

from app.models.resume import Resume
from app.models.job import JobDescription

from app.api.routes import router


# ============================================================
# Create Database Tables
# ============================================================

Base.metadata.create_all(bind=engine)


# ============================================================
# FastAPI Application
# ============================================================

app = FastAPI(
    title="AI Resume Assessment API",
    description="Resume assessment and job matching system",
    version="1.0.0"
)


# ============================================================
# Include API Routes
# ============================================================

app.include_router(router)


# ============================================================
# Home
# ============================================================

@app.get("/")
def home():
    return {
        "message": "AI Resume Assessment API is running"
    }


# ============================================================
# Health Check
# ============================================================

@app.get("/health")
def health():

    try:

        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected"
        }

    except Exception as e:

        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }
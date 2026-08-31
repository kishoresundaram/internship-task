from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.job import Job
from app.schemas.job import JobCreate, JobResponse

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)


@router.post("/", response_model=JobResponse)
def create_job(
    job_data: JobCreate,
    db: Session = Depends(get_db)
):
    job = Job(
        title=job_data.title,
        company=job_data.company,
        description=job_data.description
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return job


@router.get("/", response_model=list[JobResponse])
def get_jobs(
    db: Session = Depends(get_db)
):
    return db.query(Job).all()
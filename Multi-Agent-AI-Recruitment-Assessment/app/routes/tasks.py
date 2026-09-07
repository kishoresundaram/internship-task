from typing import Any

from fastapi import APIRouter

from app.services.job_status_service import JobStatusService
from app.tasks.assessment_tasks import (
    celery_app,
    process_assessment,
)

router = APIRouter(
    prefix="/tasks",
    tags=["Background Processing"],
)


@router.post("/assessment")
async def start_assessment(
    candidate_id: int,
    job_description_id: int,
) -> dict[str, Any]:

    task = process_assessment.delay(
        candidate_id,
        job_description_id,
    )

    return {
        "status": "accepted",
        "task_id": task.id,
        "message": "Assessment processing started.",
    }


@router.get("/assessment/{task_id}")
async def get_assessment_status(
    task_id: str,
) -> dict[str, Any]:

    return JobStatusService.get_status(
        task_id,
        celery_app,
    )
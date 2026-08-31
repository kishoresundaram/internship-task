from datetime import datetime

from pydantic import BaseModel, Field


class ReportResponse(BaseModel):
    id: int
    session_id: int

    overall_score: float = Field(..., ge=0, le=10)

    strengths: str | None
    skill_gaps: str | None
    recommendations: str | None
    competency_summary: str | None
    transcript: str | None

    responsible_ai_note: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
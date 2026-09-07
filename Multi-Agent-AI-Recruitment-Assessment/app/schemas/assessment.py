from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AssessmentCreate(BaseModel):
    candidate_id: int
    job_description_id: int


class AssessmentUpdate(BaseModel):
    status: str | None = None
    technical_score: float | None = Field(default=None, ge=0, le=100)
    qa_score: float | None = Field(default=None, ge=0, le=100)
    coding_score: float | None = Field(default=None, ge=0, le=100)
    communication_score: float | None = Field(default=None, ge=0, le=100)
    overall_score: float | None = Field(default=None, ge=0, le=100)
    recommendation: str | None = None


class AssessmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    candidate_id: int
    job_description_id: int
    status: str
    technical_score: float | None = None
    qa_score: float | None = None
    coding_score: float | None = None
    communication_score: float | None = None
    overall_score: float | None = None
    recommendation: str | None = None
    created_at: datetime
    updated_at: datetime
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class JobDescriptionCreate(BaseModel):
    job_title: str
    company: str | None = None
    description: str
    required_skills: str | None = None
    experience_required: str | None = None
    location: str | None = None


class JobDescriptionResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int

    job_title: str

    company: str | None = None

    description: str

    required_skills: str | None = None

    preferred_skills: list | None = None

    experience_required: str | None = None

    education_required: list | None = None

    responsibilities: list | None = None

    qualifications: list | None = None

    location: str | None = None

    employment_type: str | None = None

    structured_profile: dict | None = None

    created_at: datetime
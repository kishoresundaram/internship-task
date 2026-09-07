from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class CandidateCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str | None = None
    resume_text: str | None = None
    structured_profile: dict | None = None


class CandidateResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    name: str
    email: EmailStr
    phone: str | None = None
    resume_text: str | None = None
    structured_profile: dict | None = None
    created_at: datetime
from pydantic import BaseModel, EmailStr


class CandidateCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str | None = None
    resume_text: str | None = None


class CandidateResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str | None = None
    resume_text: str | None = None

    class Config:
        from_attributes = True
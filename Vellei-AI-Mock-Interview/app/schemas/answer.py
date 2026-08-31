from datetime import datetime

from pydantic import BaseModel, Field


class AnswerCreate(BaseModel):
    question_id: int = Field(..., gt=0)
    answer_text: str = Field(..., min_length=1, max_length=10000)


class AnswerResponse(BaseModel):
    id: int
    session_id: int
    question_id: int
    answer_text: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
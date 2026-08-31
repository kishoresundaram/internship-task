from datetime import datetime

from pydantic import BaseModel


class QuestionResponse(BaseModel):
    id: int
    session_id: int
    question_text: str
    competency: str
    difficulty: str
    question_type: str
    sequence_number: int
    is_followup: bool
    parent_question_id: int | None
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
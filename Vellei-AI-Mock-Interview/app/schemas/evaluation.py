from pydantic import BaseModel


class AnswerSubmission(BaseModel):
    candidate_id: int
    question: str
    answer: str
    job_title: str


class EvaluationResponse(BaseModel):
    candidate_id: int
    question: str
    answer: str
    score: float
    feedback: str
    strengths: list[str]
    improvements: list[str]
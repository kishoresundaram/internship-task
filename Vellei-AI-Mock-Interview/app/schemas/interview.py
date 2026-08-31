from pydantic import BaseModel


class InterviewQuestionRequest(BaseModel):
    candidate_id: int
    job_title: str
    difficulty: str = "medium"


class InterviewStartRequest(BaseModel):
    candidate_id: int
    job_title: str
    difficulty: str = "medium"


class InterviewStartResponse(BaseModel):
    interview_id: int
    candidate_id: int
    candidate_name: str
    job_title: str
    difficulty: str
    status: str
    question: str


class InterviewAnswerRequest(BaseModel):
    interview_id: int
    answer: str


class InterviewAnswerResponse(BaseModel):
    interview_id: int
    question: str
    answer: str
    score: float
    feedback: str
    strengths: list[str]
    improvements: list[str]
    next_question: str | None
    status: str
from fastapi import APIRouter
from pydantic import BaseModel

from app.modules.rag import answer_from_job_description


router = APIRouter()


class RAGRequest(BaseModel):
    question: str


@router.post("/ask")
def ask_job_description(request: RAGRequest):

    answer = answer_from_job_description(
        request.question
    )

    return {
        "question": request.question,
        "answer": answer
    }
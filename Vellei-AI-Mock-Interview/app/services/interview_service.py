from app.services.ai_service import generate_interview_question


def get_next_question(
    candidate_name: str,
    resume_text: str,
    job_title: str,
    difficulty: str
) -> str:

    return generate_interview_question(
        candidate_name=candidate_name,
        resume_text=resume_text,
        job_title=job_title,
        difficulty=difficulty
    )
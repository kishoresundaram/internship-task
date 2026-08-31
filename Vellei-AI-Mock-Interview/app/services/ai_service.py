import os

from google import genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not configured")

client = genai.Client(api_key=GEMINI_API_KEY)


def generate_interview_question(
    candidate_name: str,
    resume_text: str,
    job_title: str,
    difficulty: str = "medium"
) -> str:

    prompt = f"""
You are Vellei AI, an intelligent AI mock interviewer.

Candidate Name:
{candidate_name}

Job Role:
{job_title}

Difficulty:
{difficulty}

Candidate Resume:
{resume_text}

Generate ONE interview question for this candidate.

Requirements:
- The question must be relevant to the job role.
- Use the candidate's resume when possible.
- Do not provide the answer.
- Do not generate multiple questions.
- Keep the question professional and realistic.
- Difficulty should match: {difficulty}.

Return only the interview question.
"""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )

    return response.text.strip()
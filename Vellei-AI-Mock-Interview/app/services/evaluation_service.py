import os
import json

from google import genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.5-flash-lite"
)

client = genai.Client(api_key=GEMINI_API_KEY)


def evaluate_answer(
    question: str,
    answer: str,
    job_title: str
):
    prompt = f"""
You are Vellei AI, an expert technical interviewer.

Job Role:
{job_title}

Interview Question:
{question}

Candidate Answer:
{answer}

Evaluate the candidate's answer.

Give:
1. A score from 0 to 10.
2. Professional feedback.
3. Three strengths.
4. Three improvements.

Return ONLY valid JSON in exactly this format:

{{
    "score": 0,
    "feedback": "feedback here",
    "strengths": [
        "strength 1",
        "strength 2",
        "strength 3"
    ],
    "improvements": [
        "improvement 1",
        "improvement 2",
        "improvement 3"
    ]
}}

Do not include markdown.
Do not include ```json.
"""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )

    text = response.text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

    try:
        result = json.loads(text)
    except json.JSONDecodeError:
        result = {
            "score": 0,
            "feedback": text,
            "strengths": [],
            "improvements": []
        }

    return result
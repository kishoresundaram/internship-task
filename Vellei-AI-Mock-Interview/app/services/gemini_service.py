import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-3.6-flash")


def generate_evaluation(question: str, answer: str):

    prompt = f"""
You are an expert technical interviewer.

Evaluate the candidate's answer to the interview question.

INTERVIEW QUESTION:
{question}

CANDIDATE ANSWER:
{answer}

Evaluate the answer based on:

1. Technical correctness
2. Relevance
3. Clarity
4. Depth
5. Practical understanding

Return ONLY valid JSON in this exact format:

{{
    "score": 0,
    "feedback": "Overall feedback",
    "strengths": "Candidate strengths",
    "improvements": "Areas for improvement"
}}

The score must be between 0 and 10.
"""

    response = model.generate_content(prompt)

    text = response.text.strip()

    if text.startswith("```json"):
        text = text.replace("```json", "", 1)
        text = text.replace("```", "", 1)

    return json.loads(text)
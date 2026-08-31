import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-3.5-flash")

def generate_reason(candidate, company):

    prompt = f"""
    Company: {company['Company']}
    Role: {company['Role']}

    Required Skills:
    {company['RequiredSkills']}

    Candidate:
    {candidate['Name']}

    Candidate Skills:
    {candidate['Skills']}

    Experience:
    {candidate['Experience']} years

    Interview Rating:
    {candidate['OverallRating']}/10

    Explain in 4 professional lines why this candidate is suitable.
    """

    try:
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        
     return f"Gemini Error: {str(e)}"


from langchain_google_genai import ChatGoogleGenerativeAI
from app.config import GEMINI_API_KEY, GEMINI_MODEL


llm = ChatGoogleGenerativeAI(
    model=GEMINI_MODEL,
    google_api_key=GEMINI_API_KEY,
    temperature=0.7
)


def get_ai_response(message: str) -> str:
    response = llm.invoke(message)
    return response.content
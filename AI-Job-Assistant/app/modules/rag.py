
from app.config import GEMINI_API_KEY, GEMINI_MODEL
from langchain_google_genai import ChatGoogleGenerativeAI

from app.utils.vector_store import search_similar_chunks


llm = ChatGoogleGenerativeAI(
    model=GEMINI_MODEL,
    google_api_key=GEMINI_API_KEY,
    temperature=0.7
)


def answer_from_job_description(question: str) -> str:

    # Search ChromaDB
    results = search_similar_chunks(
        query=question,
        top_k=3
    )

    documents = results.get("documents", [[]])[0]

    if not documents:
        return "I could not find relevant information in the job description."

    # Combine retrieved chunks
    context = "\n\n".join(documents)

    # Create RAG prompt
    prompt = f"""
You are an AI Job Assistant.

Answer the candidate's question using ONLY the information
provided in the job description context below.

If the answer is not available in the context, say:
"I could not find that information in the job description."

Job Description Context:
{context}

Candidate Question:
{question}

Give a clear and concise answer.
"""

    # Send context + question to Gemini
    response = llm.invoke(prompt)

    # Gemini may return normal text or structured content
    if isinstance(response.content, str):
        return response.content

    if isinstance(response.content, list):

        text_parts = []

        for item in response.content:

            if isinstance(item, dict) and "text" in item:
                text_parts.append(item["text"])

        return " ".join(text_parts)

    return str(response.content)

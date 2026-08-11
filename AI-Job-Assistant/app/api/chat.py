
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.config import GEMINI_API_KEY, GEMINI_MODEL

from app.database.database import (
    save_message,
    get_conversation_history
)

from app.modules.memory import (
    save_user_memory,
    get_user_memories
)

from app.api.dependencies import get_current_user

from langchain_google_genai import ChatGoogleGenerativeAI


router = APIRouter()


# Gemini LLM
llm = ChatGoogleGenerativeAI(
    model=GEMINI_MODEL,
    google_api_key=GEMINI_API_KEY,
    temperature=0.7
)


# Chat request
class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"


# Extract long-term memory
def extract_memory(message: str):

    message_lower = message.lower()

    memories = {}

    # Preferred programming language
    if "preferred programming language is" in message_lower:

        value = message.split(
            "preferred programming language is",
            1
        )[1].strip()

        memories["preferred_language"] = value

    # Preferred language
    elif "preferred language is" in message_lower:

        value = message.split(
            "preferred language is",
            1
        )[1].strip()

        memories["preferred_language"] = value

    # Career interest
    if "interested in" in message_lower:

        value = message_lower.split(
            "interested in",
            1
        )[1].strip()

        memories["career_interest"] = value

    return memories


# Protected Chat API
@router.post("/chat")
def chat(
    request: ChatRequest,
    current_user: dict = Depends(get_current_user)
):

    # Get authenticated user
    user_id = current_user["user_id"]

    username = current_user["username"]


    # Get previous conversation
    history = get_conversation_history(
        request.session_id
    )


    # Get long-term memories
    memories = get_user_memories(
        str(user_id)
    )


    # Build conversation history
    conversation = ""

    for role, message in history:

        conversation += f"{role}: {message}\n"


    # Build long-term memory context
    memory_context = ""

    for key, value in memories.items():

        memory_context += f"{key}: {value}\n"


    # Add current message
    conversation += f"user: {request.message}\n"


    # Build prompt
    prompt = f"""
You are an AI Job Assistant.

The current authenticated user is:
Username: {username}

Use both the conversation history and the user's
long-term memory to provide personalized answers.

Long-Term User Memory:
{memory_context}

Conversation History:
{conversation}

Current User Message:
{request.message}

Give a helpful and concise answer.
"""


    # Generate response
    response = llm.invoke(prompt)


    # Convert Gemini response to plain text
    if isinstance(response.content, str):

        answer = response.content

    elif isinstance(response.content, list):

        text_parts = []

        for item in response.content:

            if isinstance(item, dict) and "text" in item:

                text_parts.append(item["text"])

        answer = " ".join(text_parts)

    else:

        answer = str(response.content)


    # Save conversation
    save_message(
        request.session_id,
        "user",
        request.message
    )

    save_message(
        request.session_id,
        "assistant",
        answer
    )


    # Extract and save long-term memory
    new_memories = extract_memory(
        request.message
    )


    for key, value in new_memories.items():

        save_user_memory(
            str(user_id),
            key,
            value
        )


    return {
        "user_id": user_id,
        "username": username,
        "session_id": request.session_id,
        "message": request.message,
        "response": answer,
        "memories_saved": new_memories
    }

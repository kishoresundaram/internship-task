import os
import tempfile

from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel

from app.modules.voice import speech_to_text
from app.modules.tts import text_to_speech

from app.config import GEMINI_API_KEY, GEMINI_MODEL
from langchain_google_genai import ChatGoogleGenerativeAI


router = APIRouter()


# Gemini LLM
llm = ChatGoogleGenerativeAI(
    model=GEMINI_MODEL,
    google_api_key=GEMINI_API_KEY,
    temperature=0.7
)


# -------------------------
# Speech-to-Text
# -------------------------

@router.post("/stt")
async def speech_to_text_api(
    audio: UploadFile = File(...)
):

    suffix = os.path.splitext(audio.filename)[1]

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=suffix
    ) as temp_file:

        temp_file.write(
            await audio.read()
        )

        temp_path = temp_file.name

    try:

        text = speech_to_text(temp_path)

        return {
            "message": "Speech converted to text successfully",
            "filename": audio.filename,
            "text": text
        }

    finally:

        if os.path.exists(temp_path):
            os.remove(temp_path)


# -------------------------
# Text-to-Speech
# -------------------------

class TTSRequest(BaseModel):
    text: str


@router.post("/tts")
async def text_to_speech_api(
    request: TTSRequest
):

    audio_path = await text_to_speech(
        request.text
    )

    return {
        "message": "Text converted to speech successfully",
        "text": request.text,
        "audio_file": audio_path
    }


# -------------------------
# Complete Voice Assistant
# -------------------------

@router.post("/assistant")
async def voice_assistant(
    audio: UploadFile = File(...)
):

    suffix = os.path.splitext(audio.filename)[1]

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=suffix
    ) as temp_file:

        temp_file.write(
            await audio.read()
        )

        temp_path = temp_file.name

    try:

        # 1. Speech → Text
        question = speech_to_text(temp_path)


        # 2. Text → Gemini
        response = llm.invoke(question)


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


        # 3. Text → Speech
        audio_path = await text_to_speech(
            answer
        )


        return {
            "message": "Voice assistant response generated successfully",
            "question": question,
            "answer": answer,
            "audio_file": audio_path
        }


    finally:

        if os.path.exists(temp_path):

            os.remove(temp_path)
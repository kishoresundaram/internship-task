import os
import tempfile
from typing import Any

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.agents.screening_agent import ScreeningAgent
from app.services.transcription_service import (
    TranscriptionService,
)

router = APIRouter(
    prefix="/screening",
    tags=["Audio Video Screening"],
)


ALLOWED_EXTENSIONS = {
    ".mp3",
    ".wav",
    ".m4a",
    ".mp4",
    ".webm",
    ".ogg",
    ".mov",
}


@router.post("/upload")
async def upload_screening_media(
    file: UploadFile = File(...),
    thread_id: str | None = Form(default=None),
) -> dict[str, Any]:

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required.",
        )

    extension = os.path.splitext(
        file.filename
    )[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported media format. "
                "Use MP3, WAV, M4A, MP4, WEBM, OGG or MOV."
            ),
        )

    file_bytes = await file.read()

    if not file_bytes:
        raise HTTPException(
            status_code=400,
            detail="Uploaded media file is empty.",
        )

    temp_path = None

    try:

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=extension,
        ) as temp_file:

            temp_file.write(file_bytes)
            temp_path = temp_file.name

        transcription_service = (
            TranscriptionService(
                model_size="base",
                device="cpu",
                compute_type="int8",
            )
        )

        transcription = (
            transcription_service.transcribe(
                temp_path
            )
        )

        transcript = transcription[
            "transcript"
        ]

        agent = ScreeningAgent()

        evaluation = agent.evaluate(
            transcript
        )

        return {
            "status": "success",
            "thread_id": thread_id,
            "filename": file.filename,
            "media_type": file.content_type,
            "transcription": transcription,
            "screening": evaluation,
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )

    finally:

        if temp_path and os.path.exists(
            temp_path
        ):
            os.remove(temp_path)
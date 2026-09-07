from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile, status
from sqlalchemy import select

from app.database import AsyncSessionLocal
from app.models.candidate import Candidate
from app.services.ai_resume_parser import AIResumeParser
from app.services.resume_service import (
    ResumeExtractionError,
    ResumeFileError,
    ResumeProcessingError,
    ResumeService,
)


router = APIRouter(
    prefix="/resume",
    tags=["Resume Processing"],
)


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


resume_service = ResumeService()
ai_resume_parser = AIResumeParser()


@router.post(
    "/upload",
    status_code=status.HTTP_201_CREATED,
)
async def upload_resume(
    file: UploadFile = File(...),
):
    """
    Upload a PDF resume and process it through
    the recruitment assessment pipeline.
    """

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Resume filename is required",
        )

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF resumes are supported",
        )

    safe_filename = Path(file.filename).name
    file_path = UPLOAD_DIR / safe_filename

    try:

        file_content = await file.read()

        if not file_content:
            raise HTTPException(
                status_code=400,
                detail="Uploaded resume is empty",
            )

        file_path.write_bytes(file_content)

        # ---------------------------------------------
        # PDF extraction + local resume processing
        # ---------------------------------------------

        basic_profile = (
            resume_service.process_resume(
                str(file_path)
            )
        )

        # ---------------------------------------------
        # Validate extracted text
        # ---------------------------------------------

        if not basic_profile.raw_text:
            raise HTTPException(
                status_code=422,
                detail=(
                    "Could not extract text "
                    "from the resume"
                ),
            )

        # ---------------------------------------------
        # AI parsing
        # ---------------------------------------------

        ai_profile = ai_resume_parser.parse(
            basic_profile.raw_text
        )

        # ---------------------------------------------
        # Candidate email
        # ---------------------------------------------

        candidate_email = (
            ai_profile.get("email")
            or basic_profile.email
        )

        if not candidate_email:
            raise HTTPException(
                status_code=422,
                detail=(
                    "Could not extract an email "
                    "address from the resume"
                ),
            )

        # ---------------------------------------------
        # Database persistence
        # ---------------------------------------------

        async with AsyncSessionLocal() as db:

            existing_result = await db.execute(
                select(Candidate).where(
                    Candidate.email
                    == candidate_email
                )
            )

            candidate = (
                existing_result.scalar_one_or_none()
            )

            candidate_name = (
                ai_profile.get("name")
                or basic_profile.name
                or "Unknown Candidate"
            )

            candidate_phone = (
                ai_profile.get("phone")
                or basic_profile.phone
            )

            if candidate:

                candidate.name = candidate_name

                candidate.phone = candidate_phone

                candidate.resume_text = (
                    basic_profile.raw_text
                )

                candidate.structured_profile = (
                    ai_profile
                )

            else:

                candidate = Candidate(
                    name=candidate_name,
                    email=candidate_email,
                    phone=candidate_phone,
                    resume_text=(
                        basic_profile.raw_text
                    ),
                    structured_profile=(
                        ai_profile
                    ),
                )

                db.add(candidate)

            await db.commit()

            await db.refresh(candidate)

        return {
            "message": (
                "Resume processed successfully"
            ),

            "candidate_id": candidate.id,

            "filename": safe_filename,

            "processing": {
                "pdf_extraction": True,
                "rule_based_parsing": True,
                "ai_parsing": True,
                "llm": "Gemini",
                "profile_persistence": True,
            },

            "profile": ai_profile,
        }

    except HTTPException:
        raise

    except ResumeFileError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except ResumeExtractionError as exc:

        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc

    except ResumeProcessingError as exc:

        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=(
                "Unexpected resume processing failure"
            ),
        ) from exc
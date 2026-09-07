from pathlib import Path

from app.agents.resume_agent import ResumeProcessingAgent, ResumeProfile
from app.utils.resume_parser import (
    clean_resume_text,
    extract_text_from_pdf,
)


class ResumeProcessingError(Exception):
    """Base exception for resume processing failures."""


class ResumeFileError(ResumeProcessingError):
    """Raised when the resume file cannot be processed."""


class ResumeExtractionError(ResumeProcessingError):
    """Raised when text cannot be extracted from a resume."""


class ResumeService:
    """
    Service layer for resume processing.

    Handles PDF extraction, text cleaning,
    and rule-based resume parsing.
    """

    def __init__(self):
        self.agent = ResumeProcessingAgent()

    def process_resume(
        self,
        file_path: str,
    ) -> ResumeProfile:

        path = Path(file_path)

        if not path.exists():
            raise ResumeFileError(
                "Resume file does not exist"
            )

        if not path.is_file():
            raise ResumeFileError(
                "Resume path is not a file"
            )

        if path.suffix.lower() != ".pdf":
            raise ResumeFileError(
                "Only PDF files are supported"
            )

        if path.stat().st_size == 0:
            raise ResumeFileError(
                "Resume file is empty"
            )

        try:
            extracted_text = extract_text_from_pdf(
                str(path)
            )

        except Exception as exc:
            raise ResumeExtractionError(
                "Failed to extract text from PDF"
            ) from exc

        if not extracted_text.strip():
            raise ResumeExtractionError(
                "No readable text found in resume"
            )

        cleaned_text = clean_resume_text(
            extracted_text
        )

        if not cleaned_text.strip():
            raise ResumeExtractionError(
                "Resume text is empty after cleaning"
            )

        try:
            profile = self.agent.process(
                cleaned_text
            )

        except Exception as exc:
            raise ResumeProcessingError(
                "Failed to parse resume"
            ) from exc

        if not profile.raw_text:
            raise ResumeProcessingError(
                "Resume parser returned empty text"
            )

        return profile
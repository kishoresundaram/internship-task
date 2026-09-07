from app.agents.job_description_agent import (
    JobDescriptionProcessingAgent,
    JobDescriptionProfile,
)


class JobDescriptionProcessingError(Exception):
    """Base exception for JD processing failures."""


class JobDescriptionValidationError(
    JobDescriptionProcessingError
):
    """Raised when JD input is invalid."""


class JobDescriptionService:
    """
    Service layer for Job Description processing.

    Handles validation, cleaning and structured
    extraction of job requirements.
    """

    def __init__(self):
        self.agent = JobDescriptionProcessingAgent()

    def process_job_description(
        self,
        job_description_text: str,
    ) -> JobDescriptionProfile:
        """
        Process raw job description text.
        """

        if not isinstance(
            job_description_text,
            str,
        ):
            raise JobDescriptionValidationError(
                "Job description must be text"
            )

        if not job_description_text.strip():
            raise JobDescriptionValidationError(
                "Job description cannot be empty"
            )

        cleaned_text = "\n".join(
            " ".join(line.split())
            for line in job_description_text.splitlines()
            if line.strip()
        )

        if not cleaned_text:
            raise JobDescriptionValidationError(
                "Job description contains no readable text"
            )

        if len(cleaned_text) < 20:
            raise JobDescriptionValidationError(
                "Job description is too short to process"
            )

        try:
            profile = self.agent.process(
                cleaned_text
            )

        except Exception as exc:
            raise JobDescriptionProcessingError(
                "Failed to process job description"
            ) from exc

        if not profile.raw_text:
            raise JobDescriptionProcessingError(
                "Job description processing returned empty text"
            )

        return profile
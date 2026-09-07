import json
import os
import re
import time
from typing import Any

from dotenv import load_dotenv
from google import genai

load_dotenv()


class AIResumeParser:
    """
    AI-powered resume parser using Google Gemini.

    Converts raw resume text into a structured candidate profile.
    """

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")

        if not self.api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is not configured in the .env file"
            )

        self.model = os.getenv(
            "GEMINI_MODEL",
            "gemini-3.6-flash",
        )

        self.client = genai.Client(
            api_key=self.api_key
        )

        self.max_retries = 3

    def parse(
        self,
        resume_text: str,
    ) -> dict[str, Any]:
        """
        Parse resume text using Gemini with retry handling.
        """

        if not resume_text.strip():
            raise ValueError(
                "Resume text cannot be empty"
            )

        prompt = self._build_prompt(
            resume_text
        )

        last_error = None

        for attempt in range(
            1,
            self.max_retries + 1,
        ):

            try:

                response = (
                    self.client.models.generate_content(
                        model=self.model,
                        contents=prompt,
                        config={
                            "temperature": 0,
                            "response_mime_type": (
                                "application/json"
                            ),
                        },
                    )
                )

                content = response.text

                if not content:
                    raise ValueError(
                        "Gemini returned an empty response"
                    )

                parsed_data = (
                    self._parse_json_response(
                        content
                    )
                )

                return self._normalize_profile(
                    parsed_data
                )

            except Exception as exc:

                last_error = exc

                error_text = str(exc).lower()

                temporary_error = (
                    "503" in error_text
                    or "unavailable" in error_text
                    or "high demand" in error_text
                    or "429" in error_text
                    or "resource exhausted" in error_text
                )

                if not temporary_error:
                    raise

                if attempt < self.max_retries:

                    wait_seconds = (
                        2 ** attempt
                    )

                    print(
                        f"Gemini temporarily unavailable. "
                        f"Retrying in {wait_seconds} seconds..."
                    )

                    time.sleep(
                        wait_seconds
                    )

        raise RuntimeError(
            "Gemini is temporarily unavailable "
            "after multiple retry attempts. "
            "Please try the resume upload again later."
        ) from last_error

    def _build_prompt(
        self,
        resume_text: str,
    ) -> str:

        return f"""
You are an expert recruitment resume parser.

Analyze the following resume and extract accurate,
structured candidate information.

Return ONLY valid JSON using exactly this structure:

{{
    "name": null,
    "email": null,
    "phone": null,
    "skills": [],
    "education": [],
    "experience": [],
    "projects": [],
    "certifications": [],
    "summary": null,
    "total_experience_years": null,
    "missing_information": []
}}

Rules:

1. Extract the candidate's full name.
2. Extract email address.
3. Extract phone number.
4. Extract technical and professional skills.
5. Extract all relevant education details.
6. Extract work experience.
7. Extract projects.
8. Extract certifications and training.
9. Create a concise professional summary.
10. Estimate total experience only when enough evidence exists.
11. If information is unavailable, use null or [].
12. Never invent information.
13. Identify important missing candidate information.
14. Return JSON only.
15. Do not use Markdown code fences.

Resume:

{resume_text}
"""

    def _parse_json_response(
        self,
        content: str,
    ) -> dict[str, Any]:

        cleaned = content.strip()

        cleaned = re.sub(
            r"^```json\s*",
            "",
            cleaned,
            flags=re.IGNORECASE,
        )

        cleaned = re.sub(
            r"^```\s*",
            "",
            cleaned,
        )

        cleaned = re.sub(
            r"\s*```$",
            "",
            cleaned,
        )

        try:

            data = json.loads(
                cleaned
            )

        except json.JSONDecodeError:

            json_match = re.search(
                r"\{.*\}",
                cleaned,
                flags=re.DOTALL,
            )

            if not json_match:

                raise ValueError(
                    "Could not extract valid JSON "
                    "from Gemini response"
                )

            try:

                data = json.loads(
                    json_match.group(0)
                )

            except json.JSONDecodeError as exc:

                raise ValueError(
                    "Gemini returned invalid JSON"
                ) from exc

        if not isinstance(
            data,
            dict,
        ):

            raise ValueError(
                "Gemini response is not "
                "a JSON object"
            )

        return data

    def _normalize_profile(
        self,
        data: dict[str, Any],
    ) -> dict[str, Any]:

        list_fields = [
            "skills",
            "education",
            "experience",
            "projects",
            "certifications",
            "missing_information",
        ]

        for field in list_fields:

            value = data.get(field)

            if value is None:

                data[field] = []

            elif isinstance(
                value,
                str,
            ):

                data[field] = [value]

            elif not isinstance(
                value,
                list,
            ):

                data[field] = [
                    str(value)
                ]

        scalar_fields = [
            "name",
            "email",
            "phone",
            "summary",
            "total_experience_years",
        ]

        for field in scalar_fields:

            if field not in data:

                data[field] = None

        return data
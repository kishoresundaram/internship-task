import re
from typing import Any


class BiasMaskingService:
    """
    Removes or masks potentially bias-inducing personal
    information before merit-based evaluation.

    The scoring pipeline should focus on qualifications,
    skills, experience, assessment performance and evidence.
    """

    PATTERNS = {
        "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        "phone": r"(?<!\d)(?:\+?\d[\d\s().-]{7,}\d)(?!\d)",
        "url": r"https?://\S+|www\.\S+",
    }

    BIAS_TERMS = {
        "male": "[GENDER_REDACTED]",
        "female": "[GENDER_REDACTED]",
        "man": "[GENDER_REDACTED]",
        "woman": "[GENDER_REDACTED]",
        "boy": "[GENDER_REDACTED]",
        "girl": "[GENDER_REDACTED]",
        "he": "[PRONOUN_REDACTED]",
        "she": "[PRONOUN_REDACTED]",
        "his": "[PRONOUN_REDACTED]",
        "her": "[PRONOUN_REDACTED]",
    }

    def mask_text(self, text: str) -> str:
        if not text:
            return ""

        masked = text

        for pattern, replacement in self.PATTERNS.items():
            masked = re.sub(
                replacement_for(pattern),
                f"[{pattern.upper()}_REDACTED]",
                masked,
                flags=re.IGNORECASE,
            )

        for term, replacement in self.BIAS_TERMS.items():
            masked = re.sub(
                rf"\b{re.escape(term)}\b",
                replacement,
                masked,
                flags=re.IGNORECASE,
            )

        return masked

    def mask_candidate_profile(
        self,
        profile: dict[str, Any],
    ) -> dict[str, Any]:

        masked = dict(profile)

        for field in [
            "name",
            "email",
            "phone",
            "address",
            "date_of_birth",
            "gender",
            "photo",
        ]:
            if field in masked:
                masked[field] = "[REDACTED]"

        for field in [
            "summary",
            "objective",
        ]:
            if isinstance(masked.get(field), str):
                masked[field] = self.mask_text(
                    masked[field]
                )

        return masked

    def create_anonymized_candidate(
        self,
        candidate: dict[str, Any],
    ) -> dict[str, Any]:

        profile = candidate.get(
            "structured_profile",
            {},
        )

        return {
            "candidate_reference": (
                f"CANDIDATE-{candidate.get('id', 'UNKNOWN')}"
            ),
            "profile": self.mask_candidate_profile(
                profile
            ),
            "skills": candidate.get(
                "skills",
                profile.get("skills", []),
            ),
            "experience": candidate.get(
                "experience",
                profile.get("experience", []),
            ),
            "education": candidate.get(
                "education",
                profile.get("education", []),
            ),
        }


def replacement_for(pattern_name: str) -> str:
    """
    Return the regex associated with a named pattern.
    """

    patterns = {
        "email": (
            r"\b[A-Za-z0-9._%+-]+@"
            r"[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
        ),
        "phone": (
            r"(?<!\d)(?:\+?\d[\d\s().-]{7,}\d)(?!\d)"
        ),
        "url": r"https?://\S+|www\.\S+",
    }

    return patterns[pattern_name]
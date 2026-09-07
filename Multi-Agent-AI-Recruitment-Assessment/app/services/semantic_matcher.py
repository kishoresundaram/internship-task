from dataclasses import dataclass, field
from typing import Any

from sentence_transformers import SentenceTransformer


@dataclass
class SemanticMatch:
    """
    Represents a semantic relationship between
    a candidate skill and a required skill.
    """

    candidate_skill: str

    required_skill: str

    similarity_score: float

    matched: bool


@dataclass
class SemanticMatchResult:
    """
    Complete semantic matching result.
    """

    matches: list[SemanticMatch] = field(
        default_factory=list
    )

    matched_skills: list[str] = field(
        default_factory=list
    )

    missing_skills: list[str] = field(
        default_factory=list
    )

    similarity_threshold: float = 0.60

    def to_dict(self) -> dict[str, Any]:

        return {
            "matches": [
                {
                    "candidate_skill": match.candidate_skill,
                    "required_skill": match.required_skill,
                    "similarity_score": match.similarity_score,
                    "matched": match.matched,
                }
                for match in self.matches
            ],
            "matched_skills": self.matched_skills,
            "missing_skills": self.missing_skills,
            "similarity_threshold": self.similarity_threshold,
        }


class SemanticSkillMatcher:
    """
    Local embedding-based semantic skill matcher.

    Uses Sentence Transformers to compare candidate
    skills with job requirements.
    """

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        similarity_threshold: float = 0.60,
    ):
        self.model_name = model_name

        self.similarity_threshold = (
            similarity_threshold
        )

        self.model = SentenceTransformer(
            model_name
        )

    def match(
        self,
        candidate_skills: list[str],
        required_skills: list[str],
    ) -> SemanticMatchResult:

        if not candidate_skills:

            return SemanticMatchResult(
                missing_skills=required_skills.copy(),
                similarity_threshold=(
                    self.similarity_threshold
                ),
            )

        if not required_skills:

            return SemanticMatchResult(
                similarity_threshold=(
                    self.similarity_threshold
                )
            )

        candidate_embeddings = (
            self.model.encode(
                candidate_skills,
                normalize_embeddings=True,
            )
        )

        required_embeddings = (
            self.model.encode(
                required_skills,
                normalize_embeddings=True,
            )
        )

        matches = []

        matched_required = set()

        for required_index, required_skill in enumerate(
            required_skills
        ):

            best_candidate = None

            best_score = -1.0

            for candidate_index, candidate_skill in enumerate(
                candidate_skills
            ):

                score = float(
                    candidate_embeddings[
                        candidate_index
                    ]
                    @ required_embeddings[
                        required_index
                    ]
                )

                if score > best_score:

                    best_score = score

                    best_candidate = (
                        candidate_skill
                    )

            is_matched = (
                best_score
                >= self.similarity_threshold
            )

            matches.append(
                SemanticMatch(
                    candidate_skill=(
                        best_candidate
                    ),
                    required_skill=(
                        required_skill
                    ),
                    similarity_score=round(
                        best_score,
                        4,
                    ),
                    matched=is_matched,
                )
            )

            if is_matched:

                matched_required.add(
                    required_skill
                )

        matched_skills = list(
            matched_required
        )

        missing_skills = [
            skill
            for skill in required_skills
            if skill not in matched_required
        ]

        return SemanticMatchResult(
            matches=matches,
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            similarity_threshold=(
                self.similarity_threshold
            ),
        )
from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class SkillGapResult:
    """
    Result of comparing candidate skills
    against job description requirements.
    """

    matched_skills: list[str] = field(
        default_factory=list
    )

    missing_skills: list[str] = field(
        default_factory=list
    )

    additional_skills: list[str] = field(
        default_factory=list
    )

    match_percentage: float = 0.0

    required_skill_count: int = 0

    matched_skill_count: int = 0

    gap_count: int = 0

    recommendation: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class SkillGapAnalysisAgent:
    """
    Compares candidate skills with the skills
    required by a job description.
    """

    def analyze(
        self,
        candidate_skills: list[str],
        required_skills: list[str],
        preferred_skills: list[str] | None = None,
    ) -> SkillGapResult:
        """
        Perform skill gap analysis.
        """

        preferred_skills = (
            preferred_skills or []
        )

        candidate_normalized = (
            self._normalize_skills(
                candidate_skills
            )
        )

        required_normalized = (
            self._normalize_skills(
                required_skills
            )
        )

        preferred_normalized = (
            self._normalize_skills(
                preferred_skills
            )
        )

        candidate_lookup = {
            self._normalize_skill_name(skill): skill
            for skill in candidate_skills
        }

        required_lookup = {
            self._normalize_skill_name(skill): skill
            for skill in required_skills
        }

        preferred_lookup = {
            self._normalize_skill_name(skill): skill
            for skill in preferred_skills
        }

        matched = []
        missing = []
        additional = []

        for normalized_skill in required_normalized:

            if normalized_skill in candidate_normalized:

                matched.append(
                    candidate_lookup.get(
                        normalized_skill,
                        normalized_skill,
                    )
                )

            else:

                missing.append(
                    required_lookup.get(
                        normalized_skill,
                        normalized_skill,
                    )
                )

        for normalized_skill in candidate_normalized:

            if normalized_skill not in required_normalized:

                additional.append(
                    candidate_lookup.get(
                        normalized_skill,
                        normalized_skill,
                    )
                )

        required_count = len(
            required_normalized
        )

        matched_count = len(
            matched
        )

        if required_count > 0:

            match_percentage = round(
                (
                    matched_count
                    / required_count
                )
                * 100,
                2,
            )

        else:

            match_percentage = 0.0

        recommendation = (
            self._generate_recommendation(
                match_percentage,
                missing,
                preferred_normalized,
                candidate_normalized,
            )
        )

        return SkillGapResult(
            matched_skills=matched,
            missing_skills=missing,
            additional_skills=additional,
            match_percentage=match_percentage,
            required_skill_count=required_count,
            matched_skill_count=matched_count,
            gap_count=len(missing),
            recommendation=recommendation,
        )

    def _normalize_skills(
        self,
        skills: list[str],
    ) -> set[str]:

        return {
            self._normalize_skill_name(skill)
            for skill in skills
            if skill
        }

    def _normalize_skill_name(
        self,
        skill: str,
    ) -> str:

        normalized = skill.lower().strip()

        aliases = {
            "postgres": "postgresql",
            "postgre sql": "postgresql",
            "node": "node.js",
            "nodejs": "node.js",
            "reactjs": "react",
            "react.js": "react",
            "vuejs": "vue",
            "vue.js": "vue",
            "js": "javascript",
            "ts": "typescript",
            "ml": "machine learning",
            "ai": "artificial intelligence",
            "gen ai": "generative ai",
            "genai": "generative ai",
            "scikit learn": "scikit-learn",
            "sklearn": "scikit-learn",
            "rest": "rest api",
            "restful api": "rest api",
            "websocket": "websockets",
        }

        return aliases.get(
            normalized,
            normalized,
        )

    def _generate_recommendation(
        self,
        match_percentage: float,
        missing_skills: list[str],
        preferred_skills: set[str],
        candidate_skills: set[str],
    ) -> str:

        preferred_matched = (
            preferred_skills.intersection(
                candidate_skills
            )
        )

        if match_percentage >= 80:

            if missing_skills:

                return (
                    "Strong skill match. "
                    "Candidate meets most required "
                    "skills but should address the "
                    "remaining skill gaps."
                )

            return (
                "Excellent skill match. "
                "Candidate meets the required "
                "technical skills."
            )

        if match_percentage >= 60:

            return (
                "Moderate skill match. "
                "Candidate has a reasonable "
                "technical foundation but has "
                "important skill gaps."
            )

        if match_percentage >= 40:

            return (
                "Partial skill match. "
                "Candidate requires significant "
                "upskilling in required areas."
            )

        return (
            "Low skill match. "
            "Candidate is missing several "
            "core required skills."
        )
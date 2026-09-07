from app.agents.skill_gap_agent import (
    SkillGapAnalysisAgent,
    SkillGapResult,
)


class SkillGapProcessingError(Exception):
    """Base exception for skill gap processing."""


class SkillGapValidationError(
    SkillGapProcessingError
):
    """Raised when skill gap input is invalid."""


class SkillGapService:
    """
    Service layer for candidate-vs-JD
    skill gap analysis.
    """

    def __init__(self):
        self.agent = SkillGapAnalysisAgent()

    def analyze(
        self,
        candidate_skills: list[str],
        required_skills: list[str],
        preferred_skills: list[str] | None = None,
    ) -> SkillGapResult:
        """
        Validate inputs and perform skill gap analysis.
        """

        if not isinstance(
            candidate_skills,
            list,
        ):
            raise SkillGapValidationError(
                "Candidate skills must be a list"
            )

        if not isinstance(
            required_skills,
            list,
        ):
            raise SkillGapValidationError(
                "Required skills must be a list"
            )

        if preferred_skills is not None:
            if not isinstance(
                preferred_skills,
                list,
            ):
                raise SkillGapValidationError(
                    "Preferred skills must be a list"
                )

        candidate_skills = [
            skill.strip()
            for skill in candidate_skills
            if isinstance(skill, str)
            and skill.strip()
        ]

        required_skills = [
            skill.strip()
            for skill in required_skills
            if isinstance(skill, str)
            and skill.strip()
        ]

        preferred_skills = [
            skill.strip()
            for skill in (preferred_skills or [])
            if isinstance(skill, str)
            and skill.strip()
        ]

        if not required_skills:
            raise SkillGapValidationError(
                "Required skills cannot be empty"
            )

        try:
            result = self.agent.analyze(
                candidate_skills=candidate_skills,
                required_skills=required_skills,
                preferred_skills=preferred_skills,
            )

        except Exception as exc:
            raise SkillGapProcessingError(
                "Failed to perform skill gap analysis"
            ) from exc

        return result
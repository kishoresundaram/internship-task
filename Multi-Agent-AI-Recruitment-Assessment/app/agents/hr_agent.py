from typing import Any

from app.services.bias_masking_service import BiasMaskingService
from app.services.merit_scoring_service import MeritScoringService


class HRAssessmentAgent:
    """
    Performs final merit-based HR assessment.

    The agent:
    1. Masks personally identifying information.
    2. Calculates weighted merit score.
    3. Produces shortlist/review/reject decision.
    """

    def __init__(self):
        self.bias_service = BiasMaskingService()
        self.scoring_service = MeritScoringService()

    def assess(
        self,
        candidate: dict[str, Any],
        skill_match: float = 0,
        technical: float = 0,
        interview: float = 0,
        coding: float = 0,
        communication: float = 0,
        star: float = 0,
        protocol: float = 0,
    ) -> dict[str, Any]:

        # Remove personal/bias-related information
        anonymized_candidate = (
            self.bias_service.create_anonymized_candidate(candidate)
        )

        # Calculate merit-based score
        merit_result = self.scoring_service.calculate(
            skill_match=skill_match,
            technical=technical,
            interview=interview,
            coding=coding,
            communication=communication,
            star=star,
            protocol=protocol,
        )

        decision = merit_result["decision"]

        if decision == "shortlist":
            hr_reason = (
                "Candidate meets the merit-based shortlisting "
                "threshold based on skills and assessment performance."
            )

        elif decision == "review":
            hr_reason = (
                "Candidate is near the decision threshold and "
                "should receive additional HR review."
            )

        else:
            hr_reason = (
                "Candidate did not meet the minimum merit-based "
                "assessment threshold."
            )

        return {
            "candidate": anonymized_candidate,
            "merit_assessment": merit_result,
            "hr_decision": decision,
            "hr_reason": hr_reason,
        }
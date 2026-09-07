from typing import Any

from app.agents.hr_agent import HRAssessmentAgent
from app.services.merit_scoring_service import MeritScoringService


class FinalAssessmentService:
    """
    Combines all assessment components into a final recruitment decision.
    """

    def __init__(self):
        self.hr_agent = HRAssessmentAgent()
        self.scoring_service = MeritScoringService()

    def calculate_final_assessment(
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

        hr_result = self.hr_agent.assess(
            candidate=candidate,
            skill_match=skill_match,
            technical=technical,
            interview=interview,
            coding=coding,
            communication=communication,
            star=star,
            protocol=protocol,
        )

        merit = hr_result["merit_assessment"]

        return {
            "candidate": hr_result["candidate"],
            "assessment": {
                "skill_match": skill_match,
                "technical": technical,
                "interview": interview,
                "coding": coding,
                "communication": communication,
                "star": star,
                "protocol": protocol,
                "overall_score": merit["overall_score"],
            },
            "recommendation": merit["recommendation"],
            "decision": hr_result["hr_decision"],
            "reason": hr_result["hr_reason"],
            "shortlisted": hr_result["hr_decision"] == "shortlist",
            "human_review_required": hr_result["hr_decision"] == "review",
        }
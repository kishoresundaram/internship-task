from typing import Any


class MeritScoringService:
    """
    Calculates the final merit score using objective
    assessment dimensions.

    No demographic or personally identifying information
    is used in the score.
    """

    WEIGHTS = {
        "skill_match": 0.20,
        "technical": 0.20,
        "interview": 0.15,
        "coding": 0.20,
        "communication": 0.10,
        "star": 0.10,
        "protocol": 0.05,
    }

    def calculate(
        self,
        skill_match: float = 0,
        technical: float = 0,
        interview: float = 0,
        coding: float = 0,
        communication: float = 0,
        star: float = 0,
        protocol: float = 0,
    ) -> dict[str, Any]:

        scores = {
            "skill_match": self._clamp(skill_match),
            "technical": self._clamp(technical),
            "interview": self._clamp(interview),
            "coding": self._clamp(coding),
            "communication": self._clamp(communication),
            "star": self._clamp(star),
            "protocol": self._clamp(protocol),
        }

        weighted_components = {
            name: round(
                scores[name] * weight,
                2,
            )
            for name, weight in self.WEIGHTS.items()
        }

        overall = round(
            sum(weighted_components.values()),
            2,
        )

        if overall >= 80:
            recommendation = "Strongly Recommended"
            decision = "shortlist"

        elif overall >= 70:
            recommendation = "Recommended"
            decision = "shortlist"

        elif overall >= 55:
            recommendation = "Needs HR Review"
            decision = "review"

        else:
            recommendation = "Not Recommended"
            decision = "reject"

        strengths = [
            name
            for name, score in scores.items()
            if score >= 80
        ]

        improvement_areas = [
            name
            for name, score in scores.items()
            if score < 60
        ]

        return {
            "scores": scores,
            "weights": self.WEIGHTS,
            "weighted_components": weighted_components,
            "overall_score": overall,
            "recommendation": recommendation,
            "decision": decision,
            "strengths": strengths,
            "improvement_areas": improvement_areas,
        }

    @staticmethod
    def _clamp(value: float) -> float:
        return round(
            max(
                0,
                min(
                    float(value or 0),
                    100,
                ),
            ),
            2,
        )
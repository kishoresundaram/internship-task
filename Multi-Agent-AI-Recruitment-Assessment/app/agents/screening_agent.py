from typing import Any

from app.services.screening_service import (
    ScreeningEvaluationService,
)


class ScreeningAgent:
    """
    AI recruitment screening agent.

    Responsible for interpreting the transcription
    evaluation and producing a screening recommendation.
    """

    def __init__(self):

        self.service = ScreeningEvaluationService()

    def evaluate(
        self,
        transcript: str,
    ) -> dict[str, Any]:

        result = self.service.evaluate(
            transcript
        )

        score = result[
            "overall_screening_score"
        ]

        if score >= 80:
            recommendation = (
                "Strong screening performance. "
                "Proceed to the next recruitment stage."
            )
            decision = "proceed"

        elif score >= 65:
            recommendation = (
                "Acceptable screening performance. "
                "Additional evaluation recommended."
            )
            decision = "review"

        else:
            recommendation = (
                "Screening performance is below "
                "the recommended threshold."
            )
            decision = "reject"

        result.update(
            {
                "screening_recommendation": recommendation,
                "screening_decision": decision,
            }
        )

        return result
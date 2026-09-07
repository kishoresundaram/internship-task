from typing import Any

from app.agents.screening_agent import ScreeningAgent


def evaluate_screening_node(
    state: dict[str, Any],
) -> dict[str, Any]:

    transcript = state.get(
        "transcript",
        "",
    )

    if not transcript:

        return {
            "errors": [
                "Interview transcript is missing."
            ],
            "current_stage": "screening_error",
        }

    agent = ScreeningAgent()

    result = agent.evaluate(
        transcript
    )

    return {
        "communication_score": result[
            "communication_score"
        ],
        "sentiment_score": result[
            "sentiment_score"
        ],
        "star_score": result[
            "star_score"
        ],
        "protocol_score": result[
            "protocol_score"
        ],
        "screening_score": result[
            "overall_screening_score"
        ],
        "screening_analysis": result,
        "current_stage": "screening_completed",
    }
from typing import Any

from app.agents.interview_agent import (
    AdaptiveInterviewAgent,
)


def generate_interview_question_node(
    state: dict[str, Any],
) -> dict[str, Any]:

    agent = AdaptiveInterviewAgent()

    questions = state.get(
        "interview_questions",
        [],
    )

    answers = state.get(
        "interview_answers",
        [],
    )

    question = agent.generate_question(
        candidate_skills=state.get(
            "candidate_skills",
            [],
        ),
        missing_skills=state.get(
            "missing_skills",
            [],
        ),
        previous_answers=answers,
    )

    questions = questions + [question]

    return {
        "interview_questions": questions,
        "current_stage": "interview_question_generated",
    }


def evaluate_interview_answer_node(
    state: dict[str, Any],
) -> dict[str, Any]:

    questions = state.get(
        "interview_questions",
        [],
    )

    answers = state.get(
        "interview_answers",
        [],
    )

    if not questions:
        return {
            "errors": [
                "No interview question available."
            ],
            "current_stage": "interview_error",
        }

    if not answers:
        return {
            "errors": [
                "No interview answer available."
            ],
            "current_stage": "interview_error",
        }

    question = questions[-1]
    answer = answers[-1]

    agent = AdaptiveInterviewAgent()

    evaluation = agent.evaluate_answer(
        question=question["question"],
        answer=answer.get(
            "answer",
            "",
        ),
        skill=question.get(
            "skill",
            "",
        ),
        difficulty=question.get(
            "difficulty",
            "easy",
        ),
    )

    updated_answer = dict(answer)

    updated_answer["evaluation"] = evaluation

    updated_answers = (
        answers[:-1]
        + [updated_answer]
    )

    scores = []

    for item in updated_answers:
        score = item.get(
            "evaluation",
            {},
        ).get(
            "score",
            0,
        )

        scores.append(score)

    interview_score = round(
        sum(scores) / len(scores),
        2,
    )

    return {
        "interview_answers": updated_answers,
        "interview_score": interview_score,
        "technical_score": interview_score,
        "current_stage": "interview_answer_evaluated",
    }


def interview_complete_node(
    state: dict[str, Any],
) -> dict[str, Any]:

    score = state.get(
        "interview_score",
        0,
    )

    if score >= 70:
        recommendation = "Proceed to next assessment stage."
    elif score >= 50:
        recommendation = "Requires additional evaluation."
    else:
        recommendation = "Interview performance below threshold."

    return {
        "recommendation": recommendation,
        "current_stage": "interview_completed",
    }


def should_continue_interview(
    state: dict[str, Any],
) -> str:

    answers = state.get(
        "interview_answers",
        [],
    )

    max_questions = 5

    if len(answers) >= max_questions:
        return "complete"

    return "continue"
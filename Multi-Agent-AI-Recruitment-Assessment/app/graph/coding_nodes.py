from typing import Any

from app.agents.coding_agent import CodingAssessmentAgent
from app.services.e2b_service import E2BSandboxService


def generate_coding_question_node(
    state: dict[str, Any],
) -> dict[str, Any]:

    agent = CodingAssessmentAgent()

    question = agent.generate_question(
        candidate_skills=state.get("candidate_skills", []),
        missing_skills=state.get("missing_skills", []),
    )

    return {
        "coding_questions": [
            question
        ],
        "current_stage": "coding_question_generated",
    }


def execute_coding_submission_node(
    state: dict[str, Any],
) -> dict[str, Any]:

    questions = state.get("coding_questions", [])
    submissions = state.get("coding_submissions", [])

    if not questions:
        return {
            "errors": ["No coding question available."],
            "current_stage": "coding_error",
        }

    if not submissions:
        return {
            "errors": ["No coding submission available."],
            "current_stage": "coding_error",
        }

    question = questions[-1]
    submission = submissions[-1]

    code = submission.get("code", "")

    if not code.strip():
        return {
            "errors": ["Coding submission is empty."],
            "current_stage": "coding_error",
        }

    sandbox = E2BSandboxService()

    execution_result = sandbox.execute_python(
        code=code,
        test_cases=question.get("test_cases", []),
    )

    agent = CodingAssessmentAgent()

    evaluation = agent.evaluate_submission(
        execution_result
    )

    updated_submission = dict(submission)

    updated_submission["evaluation"] = evaluation

    updated_submissions = submissions[:-1] + [
        updated_submission
    ]

    return {
        "coding_submissions": updated_submissions,
        "coding_score": evaluation["coding_score"],
        "current_stage": "coding_completed",
    }
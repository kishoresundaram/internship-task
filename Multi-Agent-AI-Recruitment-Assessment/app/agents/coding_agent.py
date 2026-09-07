from typing import Any


class CodingAssessmentAgent:
    """
    Generates adaptive coding questions and evaluates
    candidate submissions.
    """

    def generate_question(
        self,
        candidate_skills: list[str],
        missing_skills: list[str],
    ) -> dict[str, Any]:

        skills = missing_skills or candidate_skills

        skill = skills[0] if skills else "Python"

        if skill.lower() in {"python", "python programming"}:

            return {
                "title": "Python Array Problem",
                "language": "python",
                "difficulty": "medium",
                "question": (
                    "Write a Python function named solve(numbers) "
                    "that returns the sum of all even numbers "
                    "in the given list."
                ),
                "function_name": "solve",
                "starter_code": (
                    "def solve(numbers):\n"
                    "    # Write your solution here\n"
                    "    pass"
                ),
                "test_cases": [
                    {
                        "input": "[1, 2, 3, 4, 5, 6]",
                        "expected_output": "12",
                    },
                    {
                        "input": "[10, 15, 20, 25]",
                        "expected_output": "30",
                    },
                    {
                        "input": "[1, 3, 5]",
                        "expected_output": "0",
                    },
                    {
                        "input": "[]",
                        "expected_output": "0",
                    },
                ],
            }

        return {
            "title": f"{skill} Coding Problem",
            "language": "python",
            "difficulty": "medium",
            "question": (
                f"Write a Python function named solve(numbers) "
                f"that processes the input using your knowledge "
                f"of {skill}."
            ),
            "function_name": "solve",
            "starter_code": (
                "def solve(numbers):\n"
                "    # Write your solution here\n"
                "    pass"
            ),
            "test_cases": [
                {
                    "input": "[1, 2, 3]",
                    "expected_output": "6",
                }
            ],
        }

    def evaluate_submission(
        self,
        execution_result: dict[str, Any],
    ) -> dict[str, Any]:

        score = execution_result.get("score", 0)

        if score >= 90:
            feedback = (
                "Excellent coding performance. "
                "The solution passed almost all test cases."
            )
        elif score >= 70:
            feedback = (
                "Good coding performance. "
                "Some edge cases may need improvement."
            )
        elif score >= 50:
            feedback = (
                "Partial solution. "
                "Review correctness and edge-case handling."
            )
        else:
            feedback = (
                "The solution requires significant improvement."
            )

        return {
            "coding_score": score,
            "passed_tests": execution_result.get("passed", 0),
            "failed_tests": execution_result.get("failed", 0),
            "total_tests": execution_result.get("total", 0),
            "feedback": feedback,
            "execution_results": execution_result.get(
                "results",
                [],
            ),
        }
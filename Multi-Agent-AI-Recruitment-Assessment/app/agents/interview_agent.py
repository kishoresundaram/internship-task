import os
from typing import Any

from dotenv import load_dotenv

load_dotenv()


class AdaptiveInterviewAgent:

    def __init__(self):
        self.model_name = os.getenv(
            "GEMINI_MODEL",
            "gemini-3.6-flash",
        )

    def generate_question(
        self,
        candidate_skills: list[str],
        missing_skills: list[str],
        previous_answers: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:

        previous_answers = previous_answers or []

        question_number = len(previous_answers) + 1

        if missing_skills:
            skill = missing_skills[
                min(
                    len(previous_answers),
                    len(missing_skills) - 1,
                )
            ]
        elif candidate_skills:
            skill = candidate_skills[
                min(
                    len(previous_answers),
                    len(candidate_skills) - 1,
                )
            ]
        else:
            skill = "Python"

        difficulty = self._difficulty(
            previous_answers
        )

        if difficulty == "easy":
            question = (
                f"Explain the fundamentals of {skill} "
                "and describe one practical use case."
            )

        elif difficulty == "medium":
            question = (
                f"How would you use {skill} to solve "
                "a real-world software engineering problem? "
                "Explain your approach and trade-offs."
            )

        else:
            question = (
                f"Design a production-level solution using "
                f"{skill}. Explain architecture, scalability, "
                "performance, security, testing and trade-offs."
            )

        return {
            "question_number": question_number,
            "question": question,
            "skill": skill,
            "difficulty": difficulty,
            "type": "technical",
        }

    def evaluate_answer(
        self,
        question: str,
        answer: str,
        skill: str,
        difficulty: str,
    ) -> dict[str, Any]:

        if not answer.strip():
            return {
                "score": 0,
                "technical_correctness": 0,
                "depth": 0,
                "relevance": 0,
                "reasoning": 0,
                "communication": 0,
                "feedback": "No answer provided.",
                "next_difficulty": "easy",
            }

        words = answer.lower().split()

        technical_terms = {
            "implementation",
            "architecture",
            "api",
            "database",
            "testing",
            "performance",
            "security",
            "scalability",
            "optimization",
            "deployment",
            "algorithm",
            "design",
            "example",
            "because",
            "trade-off",
        }

        matched = sum(
            1 for term in technical_terms
            if term in words
        )

        score = 45

        score += min(matched * 4, 28)

        if len(words) >= 40:
            score += 8

        if len(words) >= 80:
            score += 9

        score = min(score, 100)

        if score >= 80:
            next_difficulty = "hard"
        elif score >= 60:
            next_difficulty = "medium"
        else:
            next_difficulty = "easy"

        return {
            "score": round(score, 2),
            "technical_correctness": round(
                score * 0.30,
                2,
            ),
            "depth": round(
                score * 0.25,
                2,
            ),
            "relevance": round(
                score * 0.20,
                2,
            ),
            "reasoning": round(
                score * 0.15,
                2,
            ),
            "communication": round(
                score * 0.10,
                2,
            ),
            "feedback": self._feedback(score),
            "next_difficulty": next_difficulty,
            "skill": skill,
            "difficulty": difficulty,
        }

    def _difficulty(
        self,
        previous_answers: list[dict[str, Any]],
    ) -> str:

        if not previous_answers:
            return "easy"

        scores = []

        for item in previous_answers:
            evaluation = item.get(
                "evaluation",
                {},
            )

            scores.append(
                evaluation.get(
                    "score",
                    0,
                )
            )

        if not scores:
            return "easy"

        average = sum(scores) / len(scores)

        if average >= 80:
            return "hard"

        if average >= 60:
            return "medium"

        return "easy"

    def _feedback(
        self,
        score: float,
    ) -> str:

        if score >= 80:
            return (
                "Strong technical answer with good "
                "reasoning and practical understanding."
            )

        if score >= 60:
            return (
                "Good answer. More technical depth "
                "and practical examples would improve it."
            )

        return (
            "The answer needs stronger technical "
            "depth, reasoning and examples."
        )
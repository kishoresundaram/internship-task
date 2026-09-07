import re
from typing import Any


class ScreeningEvaluationService:
    """
    Evaluates interview transcripts for:

    - Communication
    - Sentiment
    - STAR structure
    - Interview protocol
    """

    STAR_KEYWORDS = {
        "situation": [
            "situation",
            "context",
            "project",
            "problem",
            "scenario",
        ],
        "task": [
            "task",
            "responsibility",
            "goal",
            "objective",
            "required",
        ],
        "action": [
            "implemented",
            "developed",
            "created",
            "designed",
            "built",
            "solved",
            "used",
            "worked",
        ],
        "result": [
            "result",
            "outcome",
            "achieved",
            "improved",
            "increased",
            "reduced",
            "success",
        ],
    }

    POSITIVE_WORDS = {
        "success",
        "achieved",
        "improved",
        "solved",
        "completed",
        "excellent",
        "effective",
        "efficient",
        "implemented",
        "developed",
    }

    NEGATIVE_WORDS = {
        "failed",
        "problem",
        "difficult",
        "unable",
        "confused",
        "bad",
        "poor",
        "mistake",
        "never",
    }

    PROTOCOL_REQUIREMENTS = {
        "introduction": [
            "hello",
            "hi",
            "experience",
            "background",
        ],
        "technical_explanation": [
            "because",
            "approach",
            "implementation",
            "technical",
            "architecture",
        ],
        "example": [
            "example",
            "for instance",
            "project",
            "experience",
        ],
        "conclusion": [
            "result",
            "outcome",
            "finally",
            "overall",
        ],
    }

    def evaluate(
        self,
        transcript: str,
    ) -> dict[str, Any]:

        normalized = transcript.lower().strip()

        if not normalized:
            return self._empty_result()

        communication = self._communication_score(
            normalized
        )

        sentiment = self._sentiment_score(
            normalized
        )

        star = self._star_score(
            normalized
        )

        protocol = self._protocol_score(
            normalized
        )

        overall = round(
            communication * 0.30
            + sentiment * 0.15
            + star * 0.30
            + protocol * 0.25,
            2,
        )

        return {
            "communication_score": communication,
            "sentiment_score": sentiment,
            "star_score": star,
            "protocol_score": protocol,
            "overall_screening_score": overall,
            "communication_analysis": self._communication_analysis(
                normalized
            ),
            "sentiment_analysis": self._sentiment_analysis(
                normalized
            ),
            "star_analysis": self._star_analysis(
                normalized
            ),
            "protocol_analysis": self._protocol_analysis(
                normalized
            ),
        }

    def _communication_score(
        self,
        text: str,
    ) -> float:

        words = re.findall(
            r"\b[\w'-]+\b",
            text,
        )

        word_count = len(words)

        if word_count == 0:
            return 0.0

        score = 50.0

        if word_count >= 30:
            score += 10

        if word_count >= 60:
            score += 10

        if word_count >= 100:
            score += 10

        technical_connectors = [
            "because",
            "therefore",
            "however",
            "first",
            "then",
            "finally",
            "for example",
        ]

        connector_count = sum(
            1
            for connector in technical_connectors
            if connector in text
        )

        score += min(
            connector_count * 3,
            15,
        )

        sentences = re.split(
            r"[.!?]+",
            text,
        )

        meaningful_sentences = [
            sentence
            for sentence in sentences
            if len(sentence.split()) >= 3
        ]

        if len(meaningful_sentences) >= 3:
            score += 5

        return round(
            min(score, 100),
            2,
        )

    def _sentiment_score(
        self,
        text: str,
    ) -> float:

        positive = sum(
            1
            for word in self.POSITIVE_WORDS
            if word in text
        )

        negative = sum(
            1
            for word in self.NEGATIVE_WORDS
            if word in text
        )

        score = 60 + (
            positive * 5
        ) - (
            negative * 5
        )

        return round(
            max(0, min(score, 100)),
            2,
        )

    def _star_score(
        self,
        text: str,
    ) -> float:

        detected = {}

        for category, keywords in self.STAR_KEYWORDS.items():

            matches = [
                keyword
                for keyword in keywords
                if keyword in text
            ]

            detected[category] = matches

        categories_present = sum(
            bool(matches)
            for matches in detected.values()
        )

        score = categories_present * 25

        return round(
            min(score, 100),
            2,
        )

    def _protocol_score(
        self,
        text: str,
    ) -> float:

        completed = {}

        for requirement, keywords in self.PROTOCOL_REQUIREMENTS.items():

            found = [
                keyword
                for keyword in keywords
                if keyword in text
            ]

            completed[requirement] = found

        completed_count = sum(
            bool(found)
            for found in completed.values()
        )

        score = (
            completed_count / len(
                self.PROTOCOL_REQUIREMENTS
            )
        ) * 100

        return round(score, 2)

    def _communication_analysis(
        self,
        text: str,
    ) -> dict[str, Any]:

        word_count = len(
            re.findall(
                r"\b[\w'-]+\b",
                text,
            )
        )

        return {
            "word_count": word_count,
            "clarity": (
                "good"
                if word_count >= 40
                else "needs improvement"
            ),
            "structure": (
                "structured"
                if any(
                    word in text
                    for word in [
                        "first",
                        "then",
                        "finally",
                    ]
                )
                else "basic"
            ),
        }

    def _sentiment_analysis(
        self,
        text: str,
    ) -> dict[str, Any]:

        positive = sum(
            word in text
            for word in self.POSITIVE_WORDS
        )

        negative = sum(
            word in text
            for word in self.NEGATIVE_WORDS
        )

        if positive > negative:
            sentiment = "positive"
        elif negative > positive:
            sentiment = "negative"
        else:
            sentiment = "neutral"

        return {
            "sentiment": sentiment,
            "positive_indicators": positive,
            "negative_indicators": negative,
        }

    def _star_analysis(
        self,
        text: str,
    ) -> dict[str, Any]:

        detected = {}

        for category, keywords in self.STAR_KEYWORDS.items():

            detected[category] = [
                keyword
                for keyword in keywords
                if keyword in text
            ]

        return {
            "situation": bool(
                detected["situation"]
            ),
            "task": bool(
                detected["task"]
            ),
            "action": bool(
                detected["action"]
            ),
            "result": bool(
                detected["result"]
            ),
            "details": detected,
        }

    def _protocol_analysis(
        self,
        text: str,
    ) -> dict[str, Any]:

        completed = {}

        for requirement, keywords in self.PROTOCOL_REQUIREMENTS.items():

            completed[requirement] = any(
                keyword in text
                for keyword in keywords
            )

        return completed

    def _empty_result(self):

        return {
            "communication_score": 0,
            "sentiment_score": 0,
            "star_score": 0,
            "protocol_score": 0,
            "overall_screening_score": 0,
            "communication_analysis": {},
            "sentiment_analysis": {},
            "star_analysis": {},
            "protocol_analysis": {},
        }
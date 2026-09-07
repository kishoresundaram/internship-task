from app.services.skill_vector_service import SkillVectorService


class SemanticSkillGapService:
    def __init__(self):
        self.vector_service = SkillVectorService()

    def analyze(
        self,
        candidate_skills: list[str],
        required_skills: list[str],
        similarity_threshold: float = 0.60,
    ) -> dict:

        if not required_skills:
            return {
                "matched_skills": [],
                "missing_skills": [],
                "additional_skills": candidate_skills,
                "match_percentage": 0.0,
                "required_skill_count": 0,
                "matched_skill_count": 0,
                "gap_count": 0,
            }

        # Remove duplicate candidate skills
        unique_candidate_skills = list(
            dict.fromkeys(
                skill.strip()
                for skill in candidate_skills
                if skill and skill.strip()
            )
        )

        # Remove duplicate required skills
        unique_required_skills = list(
            dict.fromkeys(
                skill.strip()
                for skill in required_skills
                if skill and skill.strip()
            )
        )

        # Store candidate skills in Qdrant
        self.vector_service.store_skills(
            skills=unique_candidate_skills,
            source="candidate",
        )

        matched_skills = []
        missing_skills = []

        # Track candidate skills already used
        used_candidate_skills = set()

        for required_skill in unique_required_skills:

            results = self.vector_service.search_skills(
                skill=required_skill,
                limit=10,
            )

            best_match = None
            best_score = 0.0

            for result in results:
                payload = result.payload or {}

                if payload.get("source") != "candidate":
                    continue

                candidate_skill = payload.get("skill")

                if not candidate_skill:
                    continue

                candidate_key = candidate_skill.lower()

                if candidate_key in used_candidate_skills:
                    continue

                score = float(result.score)

                if score > best_score:
                    best_score = score
                    best_match = candidate_skill

            if (
                best_match
                and best_score >= similarity_threshold
            ):
                matched_skills.append(
                    {
                        "required_skill": required_skill,
                        "candidate_skill": best_match,
                        "similarity_score": round(
                            best_score,
                            4,
                        ),
                    }
                )

                used_candidate_skills.add(
                    best_match.lower()
                )

            else:
                missing_skills.append(
                    required_skill
                )

        additional_skills = [
            skill
            for skill in unique_candidate_skills
            if skill.lower() not in used_candidate_skills
        ]

        matched_count = len(matched_skills)
        required_count = len(unique_required_skills)

        match_percentage = (
            matched_count / required_count
        ) * 100

        return {
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "additional_skills": additional_skills,
            "match_percentage": round(
                match_percentage,
                2,
            ),
            "required_skill_count": required_count,
            "matched_skill_count": matched_count,
            "gap_count": len(missing_skills),
        }
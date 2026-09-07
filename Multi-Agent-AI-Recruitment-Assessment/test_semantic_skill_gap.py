from pprint import pprint

from app.services.semantic_skill_gap_service import (
    SemanticSkillGapService,
)


def main():
    print("Initializing semantic skill-gap service...")

    service = SemanticSkillGapService()

    candidate_skills = [
        "Python",
        "FastAPI",
        "PostgreSQL",
        "Machine Learning",
        "Git",
    ]

    required_skills = [
        "Python Programming",
        "FastAPI",
        "SQL Database",
        "Machine Learning",
        "Docker",
    ]

    print("\nCandidate skills:")
    for skill in candidate_skills:
        print("-", skill)

    print("\nRequired skills:")
    for skill in required_skills:
        print("-", skill)

    print("\nRunning semantic skill-gap analysis...")

    result = service.analyze(
        candidate_skills=candidate_skills,
        required_skills=required_skills,
        similarity_threshold=0.60,
    )

    print("\nResult:")
    pprint(result)

    assert "matched_skills" in result
    assert "missing_skills" in result
    assert "match_percentage" in result

    print("\nSTEP 4.12 TEST PASSED")


if __name__ == "__main__":
    main()
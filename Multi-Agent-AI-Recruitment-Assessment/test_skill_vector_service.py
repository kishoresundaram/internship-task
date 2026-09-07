from app.services.skill_vector_service import SkillVectorService


def main():
    print("Initializing skill vector service...")

    service = SkillVectorService()

    skills = [
        "Python",
        "FastAPI",
        "PostgreSQL",
        "Machine Learning",
        "Generative AI",
        "Docker",
        "Git",
    ]

    print("\nStoring skills:")

    for skill in skills:
        print("-", skill)

    service.store_skills(
        skills=skills,
        source="test",
    )

    print("\nSkills stored successfully.")

    query = "Python programming"

    print(f"\nSearching for: {query}")

    results = service.search_skills(
        skill=query,
        limit=5,
    )

    print("\nSimilar skills:")

    for result in results:
        print(
            f"Skill: {result.payload.get('skill')}, "
            f"Score: {result.score:.4f}"
        )

    assert len(results) > 0

    print("\nSTEP 4.11 TEST PASSED")


if __name__ == "__main__":
    main()
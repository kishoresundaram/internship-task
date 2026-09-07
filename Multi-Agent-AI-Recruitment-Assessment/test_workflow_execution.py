from app.graph.workflow import build_recruitment_graph


def main():

    print("Starting multi-agent recruitment workflow...\n")

    graph = build_recruitment_graph()

    initial_state = {
        "resume_text": """
        Kishore Sundaram
        Email: kishore@example.com

        Skills:
        Python, FastAPI, SQL, PostgreSQL, Machine Learning,
        Generative AI, Git, Docker

        Education:
        B.Tech Computer Science and Engineering

        Experience:
        Software Development Intern
        Worked on Python and AI-based applications.
        """,

        "job_description_text": """
        AI Software Engineer

        Required Skills:
        Python, FastAPI, PostgreSQL, Machine Learning,
        Generative AI, Docker

        Responsibilities:
        Develop AI applications.
        Build backend APIs.
        Work with databases and machine learning systems.
        """,

        "errors": [],
    }

    print("Running workflow...\n")

    result = graph.invoke(
        initial_state,
        config={
            "configurable": {
                "thread_id": "test-recruitment-001"
            }
        },
    )

    print("Workflow completed successfully.\n")

    print("Current Stage:")
    print(result.get("current_stage"))

    print("\nCandidate Skills:")
    print(result.get("candidate_skills"))

    print("\nRequired Skills:")
    print(result.get("required_skills"))

    print("\nMatched Skills:")
    print(result.get("matched_skills"))

    print("\nMissing Skills:")
    print(result.get("missing_skills"))

    print("\nAdditional Skills:")
    print(result.get("additional_skills"))

    print("\nSkill Match Percentage:")
    print(result.get("skill_match_percentage"))

    print("\nErrors:")
    print(result.get("errors"))

    assert result.get("resume_profile") is not None
    assert result.get("job_description_profile") is not None
    assert result.get("matched_skills") is not None
    assert result.get("missing_skills") is not None

    print("\nSTEP 5.6 TEST PASSED")


if __name__ == "__main__":
    main()
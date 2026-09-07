from app.graph.workflow import build_recruitment_graph


def main():
    print("Building recruitment graph...")

    graph = build_recruitment_graph()

    print("Recruitment graph compiled successfully.")

    assert graph is not None

    print("\nGraph nodes:")

    for node in graph.nodes:
        print("-", node)

    assert "resume_agent" in graph.nodes
    assert "job_description_agent" in graph.nodes
    assert "skill_gap_agent" in graph.nodes

    print("\nWorkflow:")

    print(
        "START → Resume Agent → "
        "Job Description Agent → "
        "Skill Gap Agent → END"
    )

    print("\nSTEP 5.3 TEST PASSED")


if __name__ == "__main__":
    main()
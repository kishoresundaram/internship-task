from app.graph.workflow import build_recruitment_graph


def main():

    print("Building conditional recruitment graph...")

    graph = build_recruitment_graph()

    print("Conditional recruitment graph compiled successfully.")

    assert graph is not None

    print("\nGraph nodes:")

    for node in graph.nodes:
        print("-", node)

    assert "resume_agent" in graph.nodes
    assert "job_description_agent" in graph.nodes
    assert "skill_gap_agent" in graph.nodes

    print("\nConditional routing:")

    print(
        "Skill Gap Agent"
        " → success → END"
    )

    print(
        "Skill Gap Agent"
        " → error → END"
    )

    print("\nSTEP 5.4 TEST PASSED")


if __name__ == "__main__":
    main()
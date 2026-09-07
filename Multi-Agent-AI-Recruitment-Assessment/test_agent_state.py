from app.graph.state import RecruitmentState
from langgraph.graph import StateGraph


def main():
    print("Creating RecruitmentState...")

    state: RecruitmentState = {
        "candidate_id": 1,
        "job_description_id": 1,
        "candidate_skills": [
            "Python",
            "FastAPI",
        ],
        "required_skills": [
            "Python",
            "FastAPI",
            "PostgreSQL",
        ],
        "current_stage": "initialized",
        "human_review_required": False,
    }

    print("State created successfully.")

    print("\nCandidate ID:", state["candidate_id"])
    print("Job Description ID:", state["job_description_id"])
    print("Candidate Skills:", state["candidate_skills"])
    print("Required Skills:", state["required_skills"])
    print("Current Stage:", state["current_stage"])

    print("\nCreating LangGraph StateGraph...")

    graph = StateGraph(RecruitmentState)

    print("StateGraph created successfully.")

    assert state["candidate_id"] == 1
    assert len(state["candidate_skills"]) == 2
    assert len(state["required_skills"]) == 3
    assert graph is not None

    print("\nSTEP 5.2 TEST PASSED")


if __name__ == "__main__":
    main()
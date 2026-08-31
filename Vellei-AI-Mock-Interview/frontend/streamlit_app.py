import streamlit as st
import requests


API_URL = "http://127.0.0.1:8000"


# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="Vellei AI Mock Interview",
    page_icon="🤖",
    layout="centered"
)


st.title("🤖 Vellei AI Mock Interview")
st.write("AI-powered technical interview practice using Gemini")


# -----------------------------
# Session State
# -----------------------------

if "candidate_id" not in st.session_state:
    st.session_state.candidate_id = None

if "interview_id" not in st.session_state:
    st.session_state.interview_id = None

if "question" not in st.session_state:
    st.session_state.question = None

if "started" not in st.session_state:
    st.session_state.started = False

if "evaluations" not in st.session_state:
    st.session_state.evaluations = []


# -----------------------------
# Candidate Details
# -----------------------------

st.header("👤 Candidate Details")

name = st.text_input(
    "Name",
    value="Kishore"
)

email = st.text_input(
    "Email",
    value="kishore3@example.com"
)

phone = st.text_input(
    "Phone",
    value="9876543213"
)

resume_text = st.text_area(
    "Resume / Skills",
    value="Python FastAPI SQL Machine Learning Generative AI"
)

job_title = st.text_input(
    "Job Title",
    value="AI Software Engineer"
)

difficulty = st.selectbox(
    "Difficulty",
    ["easy", "medium", "hard"],
    index=1
)


# -----------------------------
# Start Interview
# -----------------------------

if st.button("🚀 Start Mock Interview"):

    try:

        # -----------------------------
        # Create Candidate
        # -----------------------------

        candidate_response = requests.post(
            f"{API_URL}/candidates/",
            json={
                "name": name,
                "email": email,
                "phone": phone,
                "resume_text": resume_text
            }
        )

        if candidate_response.status_code not in [200, 201]:

            st.error(
                f"Candidate creation failed: "
                f"{candidate_response.text}"
            )

            st.stop()


        candidate_data = candidate_response.json()

        candidate_id = candidate_data.get("id")


        if not candidate_id:

            st.error(
                "Candidate ID was not returned."
            )

            st.stop()


        st.session_state.candidate_id = candidate_id


        # -----------------------------
        # Start Interview
        # -----------------------------

        interview_response = requests.post(
            f"{API_URL}/interview/start",
            json={
                "candidate_id": candidate_id,
                "job_title": job_title,
                "difficulty": difficulty
            }
        )


        if interview_response.status_code != 200:

            st.error(
                f"Interview creation failed: "
                f"{interview_response.text}"
            )

            st.stop()


        interview_data = interview_response.json()


        # -----------------------------
        # Store Interview Data
        # -----------------------------

        st.session_state.interview_id = (
            interview_data.get("interview_id")
        )

        st.session_state.question = (
            interview_data.get("question")
        )

        st.session_state.started = True

        st.session_state.evaluations = []


        st.success(
            "Interview started successfully!"
        )


    except requests.exceptions.ConnectionError:

        st.error(
            "Cannot connect to FastAPI. "
            "Make sure the backend server is running."
        )


# -----------------------------
# Interview Section
# -----------------------------

if st.session_state.started:

    st.divider()

    st.header("🎯 Mock Interview")

    st.subheader("AI Interview Question")

    st.info(
        st.session_state.question
    )


    # -----------------------------
    # Candidate Answer
    # -----------------------------

    answer = st.text_area(
        "Your Answer",
        height=180,
        placeholder="Type your technical answer here..."
    )


    # -----------------------------
    # Submit Answer
    # -----------------------------

    if st.button("📤 Submit Answer"):

        if not answer.strip():

            st.warning(
                "Please enter an answer before submitting."
            )

        else:

            try:

                evaluation_response = requests.post(
                    f"{API_URL}/evaluation/",
                    json={
                        "interview_id": (
                            st.session_state.interview_id
                        ),
                        "question": (
                            st.session_state.question
                        ),
                        "answer": answer
                    }
                )


                if evaluation_response.status_code != 200:

                    st.error(
                        "Evaluation failed: "
                        f"{evaluation_response.text}"
                    )


                else:

                    evaluation_data = (
                        evaluation_response.json()
                    )


                    if evaluation_data.get("success"):

                        score = evaluation_data.get(
                            "score",
                            0
                        )

                        feedback = evaluation_data.get(
                            "feedback",
                            ""
                        )

                        strengths = evaluation_data.get(
                            "strengths",
                            ""
                        )

                        improvements = evaluation_data.get(
                            "improvements",
                            ""
                        )


                        # Store evaluation
                        st.session_state.evaluations.append(
                            evaluation_data
                        )


                        # -----------------------------
                        # Display Result
                        # -----------------------------

                        st.success(
                            f"Answer evaluated! "
                            f"Score: {score}/10"
                        )


                        st.subheader(
                            "📊 AI Evaluation"
                        )


                        st.write(
                            f"**Score:** {score}/10"
                        )

                        st.write(
                            f"**Feedback:** {feedback}"
                        )

                        st.write(
                            f"**Strengths:** {strengths}"
                        )

                        st.write(
                            f"**Improvements:** "
                            f"{improvements}"
                        )


                    else:

                        st.error(
                            evaluation_data.get(
                                "message",
                                "Evaluation failed"
                            )
                        )


            except requests.exceptions.ConnectionError:

                st.error(
                    "Cannot connect to FastAPI."
                )


# -----------------------------
# Final Report
# -----------------------------

if (
    st.session_state.candidate_id
    and len(st.session_state.evaluations) > 0
):

    st.divider()

    st.header("📋 Interview Report")


    if st.button("📊 Generate Final Report"):

        try:

            report_response = requests.get(
                f"{API_URL}/report/"
                f"{st.session_state.candidate_id}"
            )


            if report_response.status_code != 200:

                st.error(
                    f"Report generation failed: "
                    f"{report_response.text}"
                )


            else:

                report = report_response.json()


                if report.get("success"):

                    # -----------------------------
                    # Summary
                    # -----------------------------

                    st.metric(
                        "Average Score",
                        f"{report.get('average_score', 0)}/10"
                    )


                    st.write(
                        f"**Candidate:** "
                        f"{report.get('candidate_name')}"
                    )


                    st.write(
                        f"**Total Questions:** "
                        f"{report.get('total_questions')}"
                    )


                    # -----------------------------
                    # Detailed Evaluation
                    # -----------------------------

                    st.subheader(
                        "📝 Detailed Evaluation"
                    )


                    for item in report.get(
                        "evaluations",
                        []
                    ):

                        with st.expander(
                            f"Question "
                            f"{item.get('evaluation_id')}"
                        ):

                            st.write(
                                "**Question:**"
                            )

                            st.write(
                                item.get("question")
                            )


                            st.write(
                                "**Answer:**"
                            )

                            st.write(
                                item.get("answer")
                            )


                            st.write(
                                f"**Score:** "
                                f"{item.get('score')}/10"
                            )


                            st.write(
                                "**Feedback:**"
                            )

                            st.write(
                                item.get("feedback")
                            )


                            st.write(
                                "**Strengths:**"
                            )

                            st.write(
                                item.get("strengths")
                            )


                            st.write(
                                "**Improvements:**"
                            )

                            st.write(
                                item.get("improvements")
                            )


                else:

                    st.error(
                        report.get(
                            "message",
                            "Report unavailable"
                        )
                    )


        except requests.exceptions.ConnectionError:

            st.error(
                "Cannot connect to FastAPI."
            )
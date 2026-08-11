
import streamlit as st
import requests


# ---------------------------------
# Configuration
# ---------------------------------

API_URL = "http://127.0.0.1:8000"


# ---------------------------------
# Page Configuration
# ---------------------------------

st.set_page_config(
    page_title="AI Job Assistant",
    page_icon="🤖",
    layout="wide"
)


# ---------------------------------
# Title
# ---------------------------------

st.title("🤖 AI Job Assistant")
st.write("Your AI-powered career assistant")


# ---------------------------------
# Sidebar
# ---------------------------------

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "Login",
        "Register",
        "Chat",
        "Job Description",
        "Voice Assistant"
    ]
)
# ---------------------------------
# Logout
# ---------------------------------

if "token" in st.session_state:

    if st.sidebar.button("🚪 Logout"):

        del st.session_state["token"]

        if "username" in st.session_state:
            del st.session_state["username"]

        st.success("Logged out successfully.")

        st.rerun()

# =================================
# REGISTER
# =================================

if page == "Register":

    st.header("📝 Create Account")

    username = st.text_input(
        "Username",
        key="register_username"
    )

    email = st.text_input(
        "Email",
        key="register_email"
    )

    password = st.text_input(
        "Password",
        type="password",
        key="register_password"
    )

    if st.button("Register"):

        if not username or not email or not password:

            st.warning(
                "Please enter username, email and password."
            )

        else:

            try:

                response = requests.post(
                    f"{API_URL}/auth/register",
                    json={
                        "username": username,
                        "email": email,
                        "password": password
                    }
                )

                if response.status_code in [200, 201]:

                    data = response.json()

                    st.success(
                        "Registration successful! 🎉"
                    )

                    st.json(data)

                else:

                    try:

                        error = response.json()

                        st.error(
                            error.get(
                                "detail",
                                "Registration failed."
                            )
                        )

                    except Exception:

                        st.error(
                            "Registration failed."
                        )

            except requests.exceptions.ConnectionError:

                st.error(
                    "Cannot connect to FastAPI. "
                    "Make sure the backend is running."
                )


# =================================
# LOGIN
# =================================

elif page == "Login":

    st.header("🔐 Login")

    username = st.text_input(
        "Username",
        key="login_username"
    )

    password = st.text_input(
        "Password",
        type="password",
        key="login_password"
    )

    if st.button("Login"):

        if not username or not password:

            st.warning(
                "Please enter username and password."
            )

        else:

            try:

                response = requests.post(
                    f"{API_URL}/auth/login",
                    json={
                        "username": username,
                        "password": password
                    }
                )

                if response.status_code == 200:

                    data = response.json()

                    # Store JWT token
                    st.session_state["token"] = data.get(
                        "access_token"
                    )

                    st.session_state["username"] = username

                    st.success(
                        "Login successful! 🎉"
                    )

                    st.write(
                        f"Welcome, **{username}**!"
                    )

                else:

                    try:

                        error = response.json()

                        st.error(
                            error.get(
                                "detail",
                                "Login failed."
                            )
                        )

                    except Exception:

                        st.error(
                            "Login failed."
                        )

            except requests.exceptions.ConnectionError:

                st.error(
                    "Cannot connect to FastAPI. "
                    "Make sure the backend is running."
                )

# =================================
# CHAT
# =================================

elif page == "Chat":

    st.header("💬 AI Chat")

    # Check if user is logged in
    if "token" not in st.session_state:

        st.warning(
            "Please login first to use the AI Chat."
        )

    else:

        st.success(
            f"Logged in as {st.session_state['username']}"
        )

        question = st.text_area(
            "Ask your question:",
            placeholder="Ask anything about your career..."
        )

        if st.button("Send"):

            if not question.strip():

                st.warning(
                    "Please enter a question."
                )

            else:

                try:

                    # JWT Authorization header
                    headers = {
                        "Authorization":
                        f"Bearer {st.session_state['token']}"
                    }

                    response = requests.post(
                        f"{API_URL}/chat",
                        json={
                            "message": question
                        },
                        headers=headers
                    )

                    if response.status_code == 200:

                        data = response.json()

                        st.subheader("🤖 AI Response")

                        st.write(data)

                    elif response.status_code == 401:

                        st.error(
                            "Authentication failed. "
                            "Please login again."
                        )

                    else:

                        try:

                            error = response.json()

                            st.error(
                                error.get(
                                    "detail",
                                    "Chat request failed."
                                )
                            )

                        except Exception:

                            st.error(
                                "Chat request failed."
                            )

                except requests.exceptions.ConnectionError:

                    st.error(
                        "Cannot connect to FastAPI. "
                        "Make sure the backend is running."
                    )

# =================================
# JOB DESCRIPTION
# =================================

if page == "Job Description":

    st.title("📄 Job Description Analyzer")

    # ---------------------------------
    # Check Login
    # ---------------------------------

    if "token" not in st.session_state:

        st.warning("⚠️ Please login first.")

    else:

        st.write(
            "Upload a Job Description and ask questions "
            "about it using AI."
        )

        # =================================
        # FILE UPLOAD
        # =================================

        st.subheader("📤 Upload Job Description")

        uploaded_file = st.file_uploader(
            "Choose a Job Description file",
            type=["pdf", "txt", "docx"]
        )

        if uploaded_file is not None:

            st.info(
                f"📄 Selected file: {uploaded_file.name}"
            )

            if st.button("🚀 Upload Job Description"):

                try:

                    # Get JWT token
                    token = st.session_state["token"]

                    # Authorization header
                    headers = {
                        "Authorization": f"Bearer {token}"
                    }

                    # Multipart file
                    files = {
                        "file": (
                            uploaded_file.name,
                            uploaded_file.getvalue(),
                            uploaded_file.type
                        )
                    }

                    with st.spinner(
                        "Processing Job Description..."
                    ):

                        response = requests.post(
                            f"{API_URL}/documents/upload-jd",
                            headers=headers,
                            files=files
                        )

                    # =================================
                    # SUCCESS
                    # =================================

                    if response.status_code == 200:

                        st.success(
                            "✅ Job Description uploaded successfully!"
                        )

                        st.session_state["jd_uploaded"] = True

                        try:
                            st.json(response.json())
                        except:
                            st.write(response.text)

                    # =================================
                    # UNAUTHORIZED
                    # =================================

                    elif response.status_code == 401:

                        st.error(
                            "❌ Session expired. Please login again."
                        )

                    # =================================
                    # VALIDATION ERROR
                    # =================================

                    elif response.status_code == 422:

                        st.error(
                            "❌ Invalid file or request."
                        )

                        try:
                            st.json(response.json())
                        except:
                            st.write(response.text)

                    # =================================
                    # OTHER ERROR
                    # =================================

                    else:

                        st.error(
                            f"❌ Upload failed "
                            f"(Status: {response.status_code})"
                        )

                        try:
                            st.json(response.json())
                        except:
                            st.write(response.text)

                except Exception as e:

                    st.error(
                        f"❌ Backend connection failed: {str(e)}"
                    )

        # =================================
        # RAG QUESTION SECTION
        # =================================

        if st.session_state.get("jd_uploaded", False):

            st.divider()

            st.subheader("💬 Ask Questions About the Job Description")

            question = st.text_input(
                "Enter your question",
                placeholder=(
                    "Example: What skills are required "
                    "for this job?"
                )
            )

            if st.button("🤖 Ask AI"):

                if not question.strip():

                    st.warning(
                        "⚠️ Please enter a question."
                    )

                else:

                    try:

                        # Get JWT token
                        token = st.session_state["token"]

                        # Headers
                        headers = {
                            "Authorization": f"Bearer {token}",
                            "Content-Type": "application/json"
                        }

                        # Request body
                        payload = {
                            "question": question
                        }

                        with st.spinner(
                            "🤖 AI is analyzing the Job Description..."
                        ):

                            response = requests.post(
                                f"{API_URL}/rag/ask",
                                headers=headers,
                                json=payload
                            )

                        # =================================
                        # SUCCESS
                        # =================================

                        if response.status_code == 200:

                            data = response.json()

                            st.success("✅ Answer generated!")

                            st.markdown("### 🤖 AI Answer")

                            st.write(
                                data.get(
                                    "answer",
                                    "No answer received."
                                )
                            )

                        # =================================
                        # UNAUTHORIZED
                        # =================================

                        elif response.status_code == 401:

                            st.error(
                                "❌ Session expired. Please login again."
                            )

                        # =================================
                        # VALIDATION ERROR
                        # =================================

                        elif response.status_code == 422:

                            st.error(
                                "❌ Invalid question format."
                            )

                            try:
                                st.json(response.json())
                            except:
                                st.write(response.text)

                        # =================================
                        # OTHER ERROR
                        # =================================

                        else:

                            st.error(
                                f"❌ RAG request failed "
                                f"(Status: {response.status_code})"
                            )

                            try:
                                st.json(response.json())
                            except:
                                st.write(response.text)

                    except Exception as e:

                        st.error(
                            f"❌ Backend connection failed: {str(e)}"
                        )

elif page == "Voice Assistant":

    st.header("🎤 Voice Assistant")

    # ---------------------------------
    # Check Login
    # ---------------------------------

    if "token" not in st.session_state:

        st.warning(
            "⚠️ Please login first to use the Voice Assistant."
        )

    else:

        st.success(
            f"Logged in as {st.session_state['username']}"
        )

        st.write(
            "🎙️ Record your question and let the AI Assistant respond."
        )

        # ---------------------------------
        # Audio Input
        # ---------------------------------

        audio = st.audio_input(
            "🎤 Record your question"
        )

        if audio is not None:

            st.audio(audio)

            if st.button("🤖 Ask Voice Assistant"):

                try:

                    # JWT Authorization
                    headers = {
                        "Authorization":
                        f"Bearer {st.session_state['token']}"
                    }

                    # Audio file
                    files = {
                        "audio": (
                            "voice.wav",
                            audio.getvalue(),
                            "audio/wav"
                        )
                    }

                    with st.spinner(
                        "🎧 Processing your voice..."
                    ):

                        response = requests.post(
                            f"{API_URL}/voice/assistant",
                            headers=headers,
                            files=files
                        )

                    # ---------------------------------
                    # SUCCESS
                    # ---------------------------------

                    if response.status_code == 200:

                        data = response.json()

                        st.success(
                            "✅ Voice response generated!"
                        )

                        st.subheader("🗣️ You said")

                        st.write(
                            data.get(
                                "question",
                                "No transcription received."
                            )
                        )

                        st.subheader("🤖 AI Response")

                        st.write(
                            data.get(
                                "answer",
                                "No answer received."
                            )
                        )

                    # ---------------------------------
                    # UNAUTHORIZED
                    # ---------------------------------

                    elif response.status_code == 401:

                        st.error(
                            "❌ Session expired. Please login again."
                        )

                    # ---------------------------------
                    # OTHER ERRORS
                    # ---------------------------------

                    else:

                        st.error(
                            f"❌ Voice request failed "
                            f"(Status: {response.status_code})"
                        )

                        try:

                            st.json(
                                response.json()
                            )

                        except Exception:

                            st.write(
                                response.text
                            )

                except requests.exceptions.ConnectionError:

                    st.error(
                        "❌ Cannot connect to FastAPI. "
                        "Make sure the backend is running."
                    )

                except Exception as e:

                    st.error(
                        f"❌ Voice processing failed: {str(e)}"
                    )

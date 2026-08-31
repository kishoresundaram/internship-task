# 🤖 Vellei AI Mock Interview

An AI-powered mock interview application that helps candidates practice technical interviews using **Google Gemini AI**.

The application allows users to create a candidate profile, start a mock interview, receive AI-generated technical questions, submit answers, and receive AI-based evaluation and feedback.

## 🚀 Features

* 👤 Candidate creation
* 📄 Resume / skills input
* 🎯 Job role selection
* ⚙️ Interview difficulty selection
* 🤖 AI-generated interview questions
* 📝 Candidate answer submission
* 📊 AI-based answer evaluation
* ⭐ Score generation
* 💬 AI feedback
* 💪 Strength identification
* 🛠️ Improvement suggestions
* 📋 Final interview report
* 🗄️ SQLite database
* ⚡ FastAPI backend
* 🖥️ Streamlit frontend

## 🏗️ Project Architecture

```text
Streamlit Frontend
        │
        ▼
   FastAPI Backend
        │
        ├── Candidate Management
        │
        ├── Interview Management
        │
        ├── Question Generation
        │
        ├── Answer Evaluation
        │
        └── Interview Report
                │
                ▼
          Google Gemini AI
                │
                ▼
             SQLite
```

## 🛠️ Technologies Used

| Technology    | Purpose                               |
| ------------- | ------------------------------------- |
| Python        | Core programming language             |
| FastAPI       | Backend REST API                      |
| Streamlit     | Frontend interface                    |
| SQLAlchemy    | ORM                                   |
| SQLite        | Database                              |
| Pydantic      | Data validation                       |
| Google Gemini | AI question generation and evaluation |
| Uvicorn       | FastAPI server                        |

## 📁 Project Structure

```text
Vellei-AI-Mock-Interview
│
├── app
│   ├── main.py
│   ├── database.py
│   │
│   ├── models
│   │   ├── candidate.py
│   │   ├── interview.py
│   │   ├── question.py
│   │   ├── answer.py
│   │   └── evaluation.py
│   │
│   ├── routes
│   │   ├── candidates.py
│   │   ├── interview.py
│   │   ├── evaluation.py
│   │   └── report.py
│   │
│   └── services
│       └── gemini_service.py
│
├── frontend
│   └── app.py
│
├── data
├── tests
├── .gitignore
├── requirements.txt
└── README.md
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/Vellei-AI-Mock-Interview.git
cd Vellei-AI-Mock-Interview
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

Windows:

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

## 🔑 Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Do not upload the `.env` file to GitHub.

## ▶️ Running the Application

### Start FastAPI Backend

From the project root:

```bash
uvicorn app.main:app --reload
```

Backend will run at:

```text
http://127.0.0.1:8000
```

FastAPI Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

### Start Streamlit Frontend

Open another terminal:

```bash
streamlit run frontend/app.py
```

The Streamlit application will open in your browser.

## 🔄 Application Workflow

```text
1. Enter Candidate Details
          ↓
2. Create Candidate
          ↓
3. Select Job Role
          ↓
4. Select Difficulty
          ↓
5. Start Mock Interview
          ↓
6. Gemini Generates Question
          ↓
7. Candidate Submits Answer
          ↓
8. Gemini Evaluates Answer
          ↓
9. Score + Feedback
          ↓
10. Generate Final Report
```

## 📊 AI Evaluation

The candidate's answer is evaluated using the following criteria:

* Technical correctness
* Relevance
* Clarity
* Depth
* Practical understanding

The system generates:

* Score out of 10
* Overall feedback
* Strengths
* Areas for improvement

## 🗄️ Database

The project currently uses **SQLite** for development.

SQLAlchemy is used as the ORM for database operations.

Main entities include:

```text
Candidate
    │
    └── Interview Session
            │
            └── Question
                    │
                    └── Answer
                            │
                            └── Evaluation
```

## 🔌 API Endpoints

### Candidate

```text
POST /candidates/
```

Creates a new candidate.

### Interview

```text
POST /interview/start
```

Starts a new mock interview and generates the first question.

### Evaluation

```text
POST /evaluation/
```

Evaluates a candidate's answer using Gemini AI.

### Report

```text
GET /report/{candidate_id}
```

Generates the candidate's interview report.

## 🧪 Testing

The backend APIs can be tested using:

* FastAPI Swagger UI
* Streamlit frontend
* Python test cases

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

## 🔐 Security

Sensitive configuration such as the Gemini API key is stored in environment variables.

The following files and folders should not be committed:

```text
.env
venv/
__pycache__/
*.pyc
*.db
```

## 🎯 Future Improvements

* 🎤 Voice-based interview
* 🔊 Text-to-speech responses
* 📄 Resume PDF upload and analysis
* 📈 Advanced candidate analytics
* 🔐 User authentication
* 🧠 Interview memory
* 📊 Advanced performance dashboard
* ☁️ Cloud deployment
* 🐘 PostgreSQL production database

## 👨‍💻 Author

**Kishore S**

### Project

**Vellei AI Mock Interview**

An AI-powered technical interview practice platform built using Python, FastAPI, Streamlit, SQLAlchemy, SQLite, and Google Gemini.

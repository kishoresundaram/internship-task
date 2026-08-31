# 🤖 AI Candidate Intelligence

An AI-powered candidate intelligence and career readiness platform that analyzes resumes, creates structured candidate profiles, identifies information gaps, recommends suitable job roles, and evaluates candidate readiness through assessments.

## 🚀 Features

* 📄 Resume PDF upload
* 🔍 Resume text extraction
* 👤 Structured candidate profile
* 📊 Profile completeness score
* ⚠️ Missing information detection
* 💬 Gap-filling questions
* 🎯 Job role recommendation
* 📈 Role matching score
* 📝 Role-specific assessment generation
* ✅ Candidate answer evaluation
* 🏆 Readiness score and level
* 📚 Interactive Swagger API documentation

## 🔄 System Workflow

```text
Resume PDF
    ↓
Resume Text Extraction
    ↓
Candidate Profile
    ↓
Completeness Analysis
    ↓
Gap Detection
    ↓
Gap-Filling Questions
    ↓
Role Recommendation
    ↓
Assessment Generation
    ↓
Answer Evaluation
    ↓
Readiness Score
```

## 🏗️ Project Structure

```text
AI-Candidate-Intelligence/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── dependencies.py
│   ├── auth.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── candidate.py
│   │   └── assessment.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── candidate.py
│   │   └── assessment.py
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── resume.py
│   │   ├── profile.py
│   │   ├── gaps.py
│   │   ├── roles.py
│   │   └── assessment.py
│   │
│   └── services/
│       ├── __init__.py
│       ├── resume_parser.py
│       ├── profile_service.py
│       ├── gap_service.py
│       ├── role_service.py
│       └── assessment_service.py
│
├── uploads/
├── data/
├── requirements.txt
├── .gitignore
└── README.md
```

## 🛠️ Technologies Used

* **Python 3.10**
* **FastAPI** – REST API development
* **Uvicorn** – Application server
* **PyMuPDF** – PDF text extraction
* **SQLAlchemy** – Database integration
* **Pydantic** – Data validation
* **Scikit-learn** – Machine learning utilities
* **NumPy** – Numerical processing
* **Passlib** – Password security support
* **Python-Jose** – JWT support

## 📡 API Endpoints

### 📄 Resume Upload

```text
POST /resume/upload
```

Uploads a PDF resume and extracts the text from the document.

### 👤 Candidate Profile

```text
POST /profile/analyze
```

Analyzes resume text and generates a structured candidate profile containing information such as:

* Name
* Email
* Phone
* Skills
* Education
* Experience
* Projects

It also calculates a profile completeness score.

### ⚠️ Gap Detection

```text
POST /gaps/analyze
```

Identifies missing candidate information and generates relevant follow-up questions.

### 🎯 Role Recommendation

```text
POST /roles/recommend
```

Matches candidate skills against predefined job-role requirements and generates ranked recommendations.

Example roles include:

* AI Engineer
* Machine Learning Engineer
* Python Backend Developer
* Data Scientist
* Full Stack Developer

### 📝 Assessment Generation

```text
POST /assessment/generate
```

Generates role-specific technical assessment questions.

### 🏆 Assessment Evaluation

```text
POST /assessment/evaluate
```

Evaluates candidate answers and produces:

* Individual question scores
* Overall readiness score
* Readiness level

## 📊 Example Readiness Result

```json
{
    "role": "AI Engineer",
    "readiness_score": 85,
    "readiness_level": "Ready"
}
```

Possible readiness levels:

```text
80–100 → Ready
60–79  → Nearly Ready
0–59   → Needs Improvement
```

## ▶️ How to Run

### 1. Clone the Repository


### 2. Open the Project


### 3. Create Virtual Environment

```bash
python -m venv venv
```

### 4. Activate Virtual Environment

Windows:

```bash
.\venv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Start the Server

```bash
uvicorn app.main:app --reload
```

### 7. Open Swagger

Visit:

```text
http://127.0.0.1:8000/docs
```

The Swagger interface allows you to test all available APIs directly from the browser.

## 🎯 Project Objective

The objective of AI Candidate Intelligence is to transform an unstructured resume into useful candidate intelligence.

The platform helps answer:

* What skills does the candidate have?
* How complete is the candidate profile?
* What information is missing?
* Which job roles best match the candidate?
* What skills are required for those roles?
* How prepared is the candidate for a selected role?

## 🔮 Future Enhancements

The project can be extended with:

* 🤖 LLM-powered resume analysis
* 🔎 Vector database and RAG pipeline
* 🧠 Long-term candidate memory
* 🔐 Complete authentication and authorization
* 🎤 Voice-based assessment
* 📚 AI-generated adaptive questions
* 📊 Advanced skill-gap analysis
* 🌐 Streamlit or React frontend
* 📈 Candidate dashboard
* ☁️ Cloud deployment
* 🗄️ Persistent candidate database
* 📊 Advanced candidate benchmarking

## 🔒 Security

Sensitive files should not be uploaded to GitHub.

The following files and folders should remain excluded:

```text
.env
venv/
uploads/
data/
__pycache__/
*.db
```


## 👨‍💻 Author

**Kishore Sundaram**

Computer Science & Engineering

## 📄 License

This project is developed for educational, learning, and portfolio purposes.

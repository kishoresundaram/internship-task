# Multi-Agent AI Recruitment Assessment

An AI-powered recruitment assessment platform that automates and streamlines the candidate evaluation process using multiple specialized AI agents.

The system evaluates candidates across **resume quality, job-skill matching, technical interviews, coding ability, communication, behavioral responses, and overall merit**, then provides an explainable HR recommendation.

## 🚀 Features

* 📄 **Resume Processing**

  * PDF resume extraction
  * Structured candidate profile generation
  * Skills, education, experience and project extraction

* 💼 **Job Description Processing**

  * Extracts required and preferred skills
  * Identifies qualifications, responsibilities and experience requirements
  * Creates a structured job profile

* 🎯 **Semantic Skill Gap Analysis**

  * Compares candidate skills with job requirements
  * Uses sentence embeddings for semantic matching
  * Identifies matched, missing and additional skills
  * Calculates skill-match percentage

* 🤖 **Multi-Agent Assessment**

  * Resume Processing Agent
  * Job Description Agent
  * Skill Gap Agent
  * Interview Agent
  * Coding Agent
  * Screening Agent
  * HR Assessment Agent

* 🧠 **Adaptive Technical Interview**

  * Generates technical questions based on candidate skills
  * Evaluates candidate answers
  * Maintains interview state using LangGraph

* 💻 **Live Coding Assessment**

  * Generates coding problems
  * Executes submitted Python code securely
  * Uses E2B Code Interpreter for code execution
  * Calculates coding performance

* 🎤 **Audio/Video Screening**

  * Supports audio and video interview recordings
  * Speech-to-text transcription using Faster-Whisper
  * Communication assessment
  * Sentiment analysis
  * STAR-method evaluation
  * Interview protocol evaluation

* ⚖️ **Bias-Aware Candidate Evaluation**

  * Masks personally identifiable information
  * Reduces potential demographic bias during assessment
  * Focuses evaluation on candidate qualifications and merit

* 📊 **Merit-Based Scoring**

  * Skill Match
  * Technical Performance
  * Interview Performance
  * Coding Performance
  * Communication
  * STAR Score
  * Protocol Score

* 👨‍💼 **Automated HR Shortlisting**

  * Strongly Recommended
  * Recommended
  * Needs HR Review
  * Not Recommended

* ⚡ **Background Task Architecture**

  * Celery-based assessment tasks
  * Redis message broker
  * Job/task status tracking

* 🔄 **Workflow Orchestration**

  * LangGraph-based recruitment workflow
  * State-based multi-agent execution
  * Checkpoint support for assessment sessions

## 🛠️ Technology Stack

| Category           | Technology            |
| ------------------ | --------------------- |
| Backend            | Python, FastAPI       |
| Database           | PostgreSQL            |
| ORM                | SQLAlchemy            |
| Database Migration | Alembic               |
| AI Workflow        | LangGraph             |
| LLM                | Google Gemini         |
| Embeddings         | Sentence Transformers |
| Vector Database    | Qdrant Cloud          |
| Resume Parsing     | PyMuPDF               |
| Speech-to-Text     | Faster-Whisper        |
| Code Execution     | E2B Code Interpreter  |
| Background Tasks   | Celery                |
| Message Broker     | Redis                 |
| API Documentation  | Swagger / OpenAPI     |

## 🏗️ System Architecture

```text
                    ┌─────────────────────┐
                    │      Candidate      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Resume Processing  │
                    │        Agent        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Job Description     │
                    │ Processing Agent    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Semantic Skill Gap  │
                    │      Analysis       │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┼─────────────┐
                 ▼             ▼             ▼
          ┌────────────┐ ┌────────────┐ ┌────────────┐
          │ Interview  │ │   Coding   │ │   Audio /  │
          │   Agent    │ │   Agent    │ │   Video    │
          └─────┬──────┘ └─────┬──────┘ │ Screening  │
                │              │         └─────┬──────┘
                └──────────────┼───────────────┘
                               ▼
                    ┌─────────────────────┐
                    │   Merit Scoring     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    HR Assessment    │
                    │       Agent         │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Shortlist / Review  │
                    │       / Reject      │
                    └─────────────────────┘
```

## 📂 Project Structure

```text
Multi-Agent-AI-Recruitment-Assessment/
│
├── alembic/
│   └── versions/
│
├── app/
│   ├── agents/
│   │   ├── coding_agent.py
│   │   ├── hr_agent.py
│   │   ├── interview_agent.py
│   │   ├── job_description_agent.py
│   │   ├── resume_agent.py
│   │   ├── screening_agent.py
│   │   └── skill_gap_agent.py
│   │
│   ├── graph/
│   │   ├── agents.py
│   │   ├── coding_nodes.py
│   │   ├── hr_nodes.py
│   │   ├── interview_nodes.py
│   │   ├── screening_nodes.py
│   │   ├── state.py
│   │   └── workflow.py
│   │
│   ├── models/
│   ├── routes/
│   ├── schemas/
│   ├── services/
│   ├── tasks/
│   ├── utils/
│   ├── database.py
│   └── main.py
│
├── requirements.txt
├── alembic.ini
└── README.md
```

## 🔌 API Modules

The FastAPI application provides endpoints for:

* Candidate management
* Job description management
* Resume processing
* Skill-gap analysis
* Semantic skill matching
* Adaptive interviews
* Coding assessments
* Audio/video screening
* HR assessment
* Final assessment
* Background assessment tasks
* Complete recruitment workflow

API documentation is available through Swagger:

```text
http://127.0.0.1:8000/docs
```

## ⚙️ Setup

### 1. Clone the Repository

```bash
git clone https://github.com/kishoresundaram/internship-task.git
cd internship-task/Multi-Agent-AI-Recruitment-Assessment
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file:

```env
DATABASE_URL=postgresql+asyncpg://postgres:YOUR_PASSWORD@localhost:5432/recruitment_assessment

GEMINI_API_KEY=YOUR_GEMINI_API_KEY
GEMINI_MODEL=gemini-3.6-flash

QDRANT_URL=YOUR_QDRANT_URL
QDRANT_API_KEY=YOUR_QDRANT_API_KEY
QDRANT_COLLECTION_NAME=recruitment_skills

E2B_API_KEY=YOUR_E2B_API_KEY

REDIS_URL=redis://localhost:6379/0
```

**Never commit the `.env` file or API keys to GitHub.**

### 5. Setup Database

Create a PostgreSQL database named:

```text
recruitment_assessment
```

Run migrations:

```bash
alembic upgrade head
```

### 6. Start the API

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

## 📊 Merit Scoring

The final candidate score is calculated using weighted assessment components:

| Assessment            | Weight |
| --------------------- | -----: |
| Skill Match           |    20% |
| Technical Performance |    20% |
| Interview             |    15% |
| Coding                |    20% |
| Communication         |    10% |
| STAR Score            |    10% |
| Protocol Score        |     5% |

### Recommendation Levels

```text
80 - 100  → Strongly Recommended
70 - 79   → Recommended
55 - 69   → Needs HR Review
0 - 54    → Not Recommended
```

## 🔐 Security & Privacy

The system includes:

* Environment-based secret management
* Candidate PII masking
* Bias-aware assessment
* Secure external code execution through E2B
* PostgreSQL database integration
* API-based architecture

API keys and credentials should always be stored in environment variables.

## 🧪 Testing

The project includes tests for major components including:

```text
test_agent_state.py
test_conditional_graph.py
test_embedding_qdrant.py
test_qdrant.py
test_recruitment_graph.py
test_semantic_skill_gap.py
test_skill_vector_service.py
test_workflow_execution.py
```

## 🎯 Project Goal

The goal of this project is to build an **AI-driven recruitment assessment system** that can reduce repetitive manual screening work while providing a structured, consistent and merit-focused candidate evaluation process.

The platform combines **Generative AI, semantic search, multi-agent workflows, automated coding evaluation, speech analysis and weighted scoring** into a single recruitment pipeline.

## 🚀 Future Enhancements

* Production deployment
* Frontend dashboard
* Advanced interview analytics
* Real-time interview monitoring
* Candidate comparison dashboard
* Recruiter authentication and role management
* Advanced analytics and reporting

## 👨‍💻 Author

**Kishore S**

B.Tech – Computer Science and Engineering

GitHub:
https://github.com/kishoresundaram

---

⭐ If you find this project useful, consider giving the repository a star.

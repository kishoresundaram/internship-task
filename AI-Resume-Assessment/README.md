# 🤖 AI-Driven Resume Assessment System

An **AI-Driven Resume Assessment System** designed to analyze resumes, conduct adaptive AI-powered interviews, evaluate technical skills, and provide a semantic ranking of the candidate.

The system is designed to make the resume assessment process more intelligent and interactive by combining **Resume Parsing, Generative AI, RAG, Vector Search, Technical Evaluation, Scoring, and Semantic Ranking**.

---

## 📌 Project Overview

Traditional resume screening mainly focuses on extracting keywords and matching them with predefined requirements.

This project aims to build a more intelligent assessment system that can:

* Upload and analyze a candidate's resume
* Extract important candidate information
* Identify missing information or gaps
* Generate personalized questions based on the resume
* Dynamically generate follow-up questions based on candidate responses
* Evaluate technical and coding skills
* Score candidate performance
* Semantically rank candidates according to their technical level

The complete workflow is designed around an AI-driven assessment approach.

---

## 🎯 Objectives

The primary objectives of this project are:

1. **Resume Analysis**

   * Extract Education
   * Extract Experience
   * Extract Skills
   * Identify missing information and gaps

2. **Adaptive AI Interview**

   * Ask baseline questions based on the resume
   * Analyze candidate responses
   * Generate personalized follow-up questions dynamically

3. **Technical Skill Evaluation**

   * Present programming problems or technical scenarios
   * Allow candidates to explain their logic and solutions
   * Evaluate their technical understanding

4. **Candidate Scoring & Ranking**

   * Evaluate candidate performance
   * Generate a score out of 10
   * Use semantic ranking to categorize the candidate's technical level

---

# 🔄 System Workflow

```text
                 ┌───────────────────────┐
                 │    Resume Upload      │
                 └───────────┬───────────┘
                             │
                             ▼
                 ┌───────────────────────┐
                 │   Resume Parsing      │
                 │ Education             │
                 │ Experience            │
                 │ Skills                │
                 └───────────┬───────────┘
                             │
                             ▼
                 ┌───────────────────────┐
                 │ Identify Information  │
                 │ Gaps / Missing Data   │
                 └───────────┬───────────┘
                             │
                             ▼
                 ┌───────────────────────┐
                 │ Adaptive AI Q&A       │
                 │ Baseline Questions    │
                 │ Follow-up Questions   │
                 └───────────┬───────────┘
                             │
                             ▼
                 ┌───────────────────────┐
                 │ Technical Evaluation  │
                 │ Coding / Scenarios    │
                 │ Logic & Solutions     │
                 └───────────┬───────────┘
                             │
                             ▼
                 ┌───────────────────────┐
                 │ AI Evaluation         │
                 │ Score /10             │
                 └───────────┬───────────┘
                             │
                             ▼
                 ┌───────────────────────┐
                 │ Semantic Ranking      │
                 │ Technical Level       │
                 └───────────────────────┘
```

---

# 🧩 Core Features

## 1. Resume Upload & Parsing

The candidate uploads their resume to the system.

The system extracts standard resume information such as:

* 🎓 Education
* 💼 Experience
* 🛠️ Skills

The system also identifies missing information and possible gaps in the resume.

## The task specifies **PyPDF2 or PyMuPDF (fitz)** for resume parsing.

## 2. Adaptive AI Dynamic Q&A

After analyzing the resume, the AI generates initial baseline questions.

The questions are based on the information available in the candidate's resume.

The system then uses the candidate's responses and previous interaction context to dynamically generate tailored follow-up questions.

This creates a more personalized assessment rather than asking every candidate the same fixed questions.

---

## 3. Technical Skill & Coding Evaluation

The system evaluates the candidate's technical knowledge.

The AI can present:

* Programming problems
* Technical scenarios
* Problem-solving situations

The candidate explains their approach, logic, or proposed solution.

The system then evaluates the candidate's technical response.

---

## 4. Scoring & Semantic Ranking

The AI evaluates the candidate's overall performance.

A numerical score can be generated, for example:

```text
Technical Assessment Score: 8/10
```

The system also uses **semantic ranking** to categorize the candidate according to their technical level.

This provides more meaningful assessment than simple keyword matching.

---

# 🏗️ Technology Stack

The task document specifies the following technology stack:

| Component           | Technology                |
| ------------------- | ------------------------- |
| Backend API         | Python + FastAPI          |
| Database            | PostgreSQL                |
| RAG & Vector Search | RAG Architecture + Qdrant |
| Resume Parser       | PyPDF2 / PyMuPDF (fitz)   |
| Search & Ranking    | Semantic Ranking System   |

---

# 🔧 Technology Details

## Python

Python is used as the primary programming language for implementing the backend and AI-related functionality.

---

## FastAPI

FastAPI is used to develop the backend API.

It provides API endpoints for handling operations such as:

* Resume upload
* Resume processing
* Assessment interaction
* Candidate evaluation

---

## PostgreSQL

PostgreSQL is the database technology specified for the project.

It can be used to store structured application information and assessment-related data.

---

## RAG

The system uses a **Retrieval-Augmented Generation (RAG)** architecture.

RAG can be used to retrieve relevant information from the candidate's resume and provide that information as context for AI-powered assessment.

---

## Qdrant

**Qdrant** is the specified vector database for the RAG and vector-search component.

It can be used to store and retrieve vector representations for semantic search.

---

## PyPDF2 / PyMuPDF

The task specifies either:

* PyPDF2
* PyMuPDF (`fitz`)

for extracting information from uploaded PDF resumes.

---

## Semantic Ranking

The system uses semantic ranking to categorize candidates according to their technical level.

Instead of relying only on exact keyword matches, semantic ranking can compare the meaning and relevance of candidate responses and assessment information.

---

# 📚 Learning Roadmap

The task document identifies the following learning areas:

### 1. FastAPI

Learn:

* FastAPI fundamentals
* API creation
* Request and response handling
* File uploads
* Backend API development

### 2. PostgreSQL

Learn:

* Database fundamentals
* Tables
* SQL queries
* Data storage
* Database integration

### 3. Vector Databases & RAG

Learn:

* Vector databases
* Embeddings
* Similarity search
* RAG concepts
* Retrieval-based AI systems

These are the learning areas explicitly mentioned in the task document.

---

# 📂 Suggested Project Structure

```text
AI-Resume-Assessment/
│
├── app/
│   ├── main.py
│   ├── api/
│   │   ├── resume.py
│   │   ├── assessment.py
│   │   └── ranking.py
│   │
│   ├── services/
│   │   ├── resume_parser.py
│   │   ├── rag_service.py
│   │   ├── assessment_service.py
│   │   └── ranking_service.py
│   │
│   ├── database/
│   │   └── database.py
│   │
│   └── models/
│       └── models.py
│
├── uploads/
│
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

> The structure above is a suggested implementation structure. The task document itself does not prescribe a specific folder structure.

---

# 🔄 Assessment Process

A typical candidate assessment can follow this sequence:

### Step 1 — Upload Resume

The candidate uploads their resume.

### Step 2 — Parse Resume

The system extracts:

```text
Education
Experience
Skills
```

### Step 3 — Identify Gaps

The system identifies missing or incomplete information.

### Step 4 — Generate Initial Questions

AI generates baseline questions based on the resume.

### Step 5 — Candidate Response

The candidate provides answers.

### Step 6 — Generate Follow-up Questions

The AI uses previous responses and interaction context to generate personalized follow-up questions.

### Step 7 — Technical Assessment

The candidate receives a programming problem or technical scenario.

### Step 8 — Evaluate Solution

The candidate explains their logic or solution.

### Step 9 — Generate Score

The AI evaluates the candidate and produces a score.

Example:

```text
Overall Technical Score: 8/10
```

### Step 10 — Semantic Ranking

The candidate is categorized according to their technical level using semantic ranking.

---

# 🧠 AI Assessment Concept

The core idea of the project is:

```text
Resume
   ↓
Resume Understanding
   ↓
Personalized Questions
   ↓
Candidate Responses
   ↓
Dynamic Follow-up Questions
   ↓
Technical Evaluation
   ↓
AI Scoring
   ↓
Semantic Ranking
```

This creates an adaptive assessment process where the interview can change according to the candidate's resume and responses.

---

# 🚀 Expected Outcome

The final system is intended to provide an AI-powered resume assessment workflow capable of:

* Resume information extraction
* Gap identification
* Personalized questioning
* Dynamic follow-up questions
* Technical problem evaluation
* Candidate scoring
* Semantic candidate ranking

The project combines backend API development, databases, resume processing, RAG/vector search, and semantic ranking into a single assessment workflow.

---

# 📖 Learning Outcomes

By working on this project, the following concepts can be learned:

* Python backend development
* FastAPI
* REST API development
* PostgreSQL
* PDF processing
* Resume information extraction
* RAG architecture
* Vector databases
* Semantic search
* Semantic ranking
* AI-powered question generation
* Technical assessment systems

---

# 🛣️ Future Enhancements

Potential extensions to the system could include:

* Candidate authentication
* Interview history
* Candidate dashboards
* Detailed skill-wise scoring
* Multiple programming languages
* Automated coding evaluation
* Voice-based interviews
* Interview reports
* Candidate comparison
* Recruiter dashboard
* Exportable assessment reports

> These are possible future enhancements and are not explicitly required by the provided task document.

---

# 👨‍💻 Project Type

**AI / Generative AI / Backend / Resume Assessment / RAG**

---

# 🏷️ Technologies

```text
Python
FastAPI
PostgreSQL
RAG
Qdrant
PyPDF2 / PyMuPDF
Vector Search
Semantic Ranking
```

---

# ⭐ Project Highlights

* 📄 AI-powered resume analysis
* 🤖 Adaptive AI questioning
* 🔄 Dynamic follow-up questions
* 💻 Technical and coding evaluation
* 📊 AI-based scoring
* 🔎 Semantic ranking
* 🧠 RAG and vector search architecture
* ⚡ FastAPI backend
* 🗄️ PostgreSQL database
* 📚 Qdrant vector database

---

## 📌 Conclusion

The **AI-Driven Resume Assessment System** provides an intelligent approach to candidate evaluation.

By combining resume parsing, adaptive AI questioning, technical assessment, scoring, RAG, vector search, and semantic ranking, the system can move beyond traditional resume screening and provide a more interactive and personalized candidate assessment experience.

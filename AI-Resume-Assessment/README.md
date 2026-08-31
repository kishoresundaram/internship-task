# 🤖 AI Resume Assessment System

An AI-powered application that analyzes resumes against job requirements and provides an intelligent assessment of the candidate's skills, strengths, and skill gaps.

---

## 📌 Project Overview

The **AI Resume Assessment System** automates the initial resume screening process using Artificial Intelligence.

The system analyzes a candidate's resume, extracts relevant skills, compares them with the required job skills, and generates an AI-based assessment.

---

## 🎯 Features

* 📄 Resume Upload
* 🔍 Resume Text Extraction
* 🧠 AI-Based Resume Analysis
* 🎯 Skill Extraction
* 🔄 Resume & Job Requirement Matching
* ✅ Matching Skills Identification
* ❌ Missing Skills Identification
* 📊 Candidate Assessment
* 💡 Skill Gap Analysis
* 🤖 AI-Based Recommendations

---

## 🔄 Project Workflow

```text
Resume Upload
      ↓
Text Extraction
      ↓
Resume Analysis
      ↓
Skill Extraction
      ↓
Job Requirement Analysis
      ↓
Skill Matching
      ↓
Skill Gap Analysis
      ↓
AI Assessment
      ↓
Final Result
```

---

## 🧠 How It Works

### 1. Resume Upload

The user uploads a candidate resume.

### 2. Text Extraction

The system extracts the text and important information from the resume.

### 3. Skill Extraction

Relevant technical and professional skills are identified.

### 4. Job Matching

Candidate skills are compared with the required skills for the target job.

### 5. Assessment

The AI generates an assessment based on the candidate's matching skills, missing skills, and overall profile.

---

## 📊 Example

### Required Skills

```text
Python
Machine Learning
Generative AI
FastAPI
SQL
Git
```

### Candidate Skills

```text
Python
Machine Learning
SQL
Git
```

### Result

**Matching Skills:**

* Python
* Machine Learning
* SQL
* Git

**Missing Skills:**

* Generative AI
* FastAPI

**Assessment:**

The candidate has a strong foundation in Python, Machine Learning, SQL, and Git, but should improve Generative AI and FastAPI skills for the target role.

---

## 🛠️ Technologies Used

* Python
* FastAPI
* Generative AI
* Natural Language Processing
* PDF/Document Processing
* REST API
* SQLite
* Git & GitHub

---

## 📂 Project Structure

```text
AI-Resume-Assessment/
│
├── app/
│   ├── main.py
│   ├── routes/
│   ├── services/
│   └── utils/
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/AI-Resume-Assessment.git
cd AI-Resume-Assessment
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

**Windows:**

```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file and add your API configuration:

```env
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=your_model_name
```

⚠️ **Do not upload `.env` to GitHub.**

Use `.env.example` instead.

---

## ▶️ Run the Project

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

FastAPI Swagger UI can be used to test the APIs.

---

## 🧪 Testing

The project can be tested using:

* FastAPI Swagger UI
* Sample resumes
* Different job descriptions
* Resume and skill matching scenarios

---

## 🚀 Future Enhancements

* ATS Resume Score
* Multiple Resume Comparison
* Candidate Ranking
* Job Recommendation
* Recruiter Dashboard
* Resume Improvement Suggestions
* Cloud Deployment

---

## 👨‍💻 Author

**Kishore S**

B.Tech – Computer Science and Engineering

---

## ⭐ Conclusion

The **AI Resume Assessment System** demonstrates how Artificial Intelligence can be used to automate resume screening, skill matching, and candidate assessment.

It provides a simple and efficient way to understand how well a candidate's profile matches a target job role.

⭐ If you like this project, consider giving the repository a star!

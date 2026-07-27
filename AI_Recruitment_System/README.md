# AI Recruitment Recommendation System

## Project Overview

The AI Recruitment Recommendation System is a backend application developed using Python and FastAPI. It helps companies identify the most suitable candidate for a job by comparing candidate skills, experience, and interview performance with company requirements.

The system reads candidate, company, and interview datasets, calculates a recommendation score, and returns the best candidate for each company.

---

## Features

- View all candidate details
- View all company details
- Find the best overall candidate
- Recommend candidates based on company requirements
- Compare candidate skills with required skills
- Calculate recommendation score
- Generate AI-based recommendation reason
- REST API using FastAPI
- Interactive API documentation using Swagger UI

---

## Technologies Used

- Python
- FastAPI
- Uvicorn
- Pandas
- NumPy
- Scikit-learn
- CountVectorizer
- Cosine Similarity

---

## Project Structure

```
AI-Recruitment-System
│
├── data
│   ├── candidates.csv
│   ├── companies.csv
│   └── interview_score.csv
│
├── main.py
├── llm.py
├── requirements.txt
└── README.md
```

---

## Installation

### Clone the repository

```bash
git clone https://github.com/yourusername/AI-Recruitment-System.git
```

Move into the project folder

```bash
cd AI-Recruitment-System
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the virtual environment

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Project

Start the FastAPI server

```bash
uvicorn main:app --reload
```

Server URL

```
http://127.0.0.1:8000
```

Swagger API Documentation

```
http://127.0.0.1:8000/docs
```

---

## API Endpoints

### Home

```
GET /
```

Returns the welcome message.

---

### Get Candidates

```
GET /candidates
```

Returns all candidate details.

---

### Get Companies

```
GET /companies
```

Returns all company details.

---

### Best Candidate

```
GET /best-candidate
```

Returns the highest-scoring candidate based on interview rating and coding score.

---

### Company Recommendation

```
GET /recommend/{company_name}
```

Example

```
GET /recommend/TCS
```

Returns the most suitable candidate for the selected company.

---

### AI Recommendation Reason

```
GET /ai-reason/{company_name}
```

Returns an AI-generated explanation for recommending a candidate.

---

## Recommendation Process

The recommendation process follows these steps:

1. Load candidate, company, and interview datasets.
2. Merge candidate and interview information.
3. Compare candidate skills with company requirements.
4. Calculate skill similarity using CountVectorizer and Cosine Similarity.
5. Calculate the final recommendation score.
6. Rank candidates based on the final score.
7. Recommend the highest-ranked candidate.

---

## Sample Output

```
Company : TCS

Recommended Candidate : Rahul

Skills : Python, SQL, Machine Learning

Skill Match : 92%

Interview Rating : 9

Final Score : 94.5
```

---

## Future Enhancements

- Resume PDF parsing
- Semantic skill matching using Sentence Transformers
- Candidate dashboard
- Company dashboard
- Authentication and Login
- Database integration (MySQL)
- Resume upload functionality
- Email notification system

---

## Author

**Kishore S**

B.Tech Computer Science and Engineering

AI Recruitment Recommendation System using FastAPI and Machine Learning.

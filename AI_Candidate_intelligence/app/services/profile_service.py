import re


SKILLS = [
    "Python",
    "Java",
    "C",
    "C++",
    "SQL",
    "MySQL",
    "PostgreSQL",
    "MongoDB",
    "FastAPI",
    "Django",
    "Flask",
    "React",
    "JavaScript",
    "HTML",
    "CSS",
    "Git",
    "GitHub",
    "Docker",
    "AWS",
    "Azure",
    "Machine Learning",
    "Deep Learning",
    "Generative AI",
    "Data Science",
    "Power BI",
    "Tableau",
    "TensorFlow",
    "PyTorch",
    "OpenCV"
]


def extract_email(text: str):
    match = re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )

    return match.group(0) if match else None


def extract_phone(text: str):
    match = re.search(
        r"(?:\+91[\s-]?)?[6-9]\d{9}",
        text
    )

    return match.group(0) if match else None


def extract_name(text: str):
    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    if lines:
        return lines[0]

    return None


def extract_skills(text: str):

    text_lower = text.lower()

    found_skills = []

    for skill in SKILLS:
        if skill.lower() in text_lower:
            found_skills.append(skill)

    return found_skills


def extract_profile(text: str):

    profile = {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "education": [],
        "experience": [],
        "projects": []
    }

    return profile


def calculate_completeness(profile: dict):

    fields = [
        "name",
        "email",
        "phone",
        "skills",
        "education",
        "experience",
        "projects"
    ]

    completed = 0

    for field in fields:

        value = profile.get(field)

        if value:
            completed += 1

    score = round((completed / len(fields)) * 100)

    missing = [
        field
        for field in fields
        if not profile.get(field)
    ]

    return score, missing
import re


SKILL_LIST = [
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
    "HTML",
    "CSS",
    "JavaScript",
    "Git",
    "GitHub",
    "Docker",
    "AWS",
    "Azure",
    "Machine Learning",
    "Deep Learning",
    "Generative AI",
    "Artificial Intelligence",
    "Data Science",
    "Data Analysis",
    "Power BI",
    "Tableau",
    "Excel",
    "Business Analytics",
    "Financial Accounting",
    "Tally",
    "Tally ERP 9",
    "MS Office",
    "Team Leadership",
    "Communication",
    "Time Management",
    "CRM",
    "CRM Tools",
    "Analytical Thinking",
]


def extract_skills(text: str):
    """
    Extract skills from resume or job description text.

    Uses word-boundary matching to prevent
    false positives such as detecting 'C'
    inside normal words.
    """

    found_skills = []

    for skill in SKILL_LIST:

        # Escape special characters such as + in C++
        escaped_skill = re.escape(skill)

        # Case-insensitive whole-word matching
        pattern = r"(?<!\w)" + escaped_skill + r"(?!\w)"

        if re.search(pattern, text, re.IGNORECASE):
            found_skills.append(skill)

    return found_skills
def detect_gaps(profile: dict):

    gaps = []

    if not profile.get("name"):
        gaps.append("name")

    if not profile.get("email"):
        gaps.append("email")

    if not profile.get("phone"):
        gaps.append("phone")

    if not profile.get("skills"):
        gaps.append("skills")

    if not profile.get("education"):
        gaps.append("education")

    if not profile.get("experience"):
        gaps.append("experience")

    if not profile.get("projects"):
        gaps.append("projects")

    return gaps


def generate_gap_questions(gaps: list):

    questions = []

    question_map = {
        "name": "What is your full name?",
        "email": "What is your email address?",
        "phone": "What is your phone number?",
        "skills": "What are your main technical skills?",
        "education": "What is your highest educational qualification?",
        "experience": "Please describe your previous work experience.",
        "projects": "Please describe your most important technical projects."
    }

    for gap in gaps:

        if gap in question_map:
            questions.append(question_map[gap])

    return questions
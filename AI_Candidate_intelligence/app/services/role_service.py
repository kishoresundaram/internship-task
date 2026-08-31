ROLE_REQUIREMENTS = {
    "AI Engineer": [
        "Python",
        "Machine Learning",
        "Deep Learning",
        "Generative AI",
        "SQL"
    ],

    "Machine Learning Engineer": [
        "Python",
        "Machine Learning",
        "Deep Learning",
        "TensorFlow",
        "PyTorch"
    ],

    "Python Backend Developer": [
        "Python",
        "FastAPI",
        "Django",
        "SQL",
        "Git"
    ],

    "Data Scientist": [
        "Python",
        "Machine Learning",
        "SQL",
        "Data Science",
        "Pandas"
    ],

    "Full Stack Developer": [
        "Python",
        "JavaScript",
        "HTML",
        "CSS",
        "React",
        "SQL"
    ]
}


def recommend_roles(skills):

    candidate_skills = {
        skill.lower()
        for skill in skills
    }

    recommendations = []

    for role, required_skills in ROLE_REQUIREMENTS.items():

        matched_skills = [
            skill
            for skill in required_skills
            if skill.lower() in candidate_skills
        ]

        score = round(
            (len(matched_skills) / len(required_skills)) * 100
        )

        recommendations.append({
            "role": role,
            "match_score": score,
            "matched_skills": matched_skills,
            "missing_skills": [
                skill
                for skill in required_skills
                if skill not in matched_skills
            ]
        })

    recommendations.sort(
        key=lambda x: x["match_score"],
        reverse=True
    )

    return recommendations
from typing import Any, TypedDict


class RecruitmentState(TypedDict, total=False):
    # Request / workflow information
    candidate_id: int
    job_description_id: int
    assessment_id: int
    coding_questions: list[dict[str, Any]]
    coding_submissions: list[dict[str, Any]]
    coding_score: float

    # Resume information
    resume_text: str
    resume_profile: dict[str, Any]

    # Job description information
    job_description_text: str
    job_description_profile: dict[str, Any]

    # Skill analysis
    candidate_skills: list[str]
    required_skills: list[str]
    matched_skills: list[dict[str, Any]]
    missing_skills: list[str]
    additional_skills: list[str]
    skill_match_percentage: float

    # Adaptive Q&A
    interview_questions: list[dict[str, Any]]
    interview_answers: list[dict[str, Any]]
    interview_score: float

    # Coding assessment
    coding_questions: list[dict[str, Any]]
    coding_submissions: list[dict[str, Any]]
    coding_score: float

    # Audio / video screening
    transcript: str
    communication_score: float
    sentiment_score: float
    star_score: float
    protocol_score: float

    # Final scoring
    technical_score: float
    overall_score: float
    recommendation: str

    # HR decision
    shortlisted: bool
    hr_decision: str
    hr_reason: str

    # Workflow control
    current_stage: str
    errors: list[str]
    human_review_required: bool

    screening_score: float
    screening_analysis: dict[str, Any]
    media_file: str
    media_type: str
import re
from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class JobDescriptionProfile:
    """
    Structured representation of a job description.
    """

    job_title: str | None = None

    company: str | None = None

    required_skills: list[str] = field(
        default_factory=list
    )

    preferred_skills: list[str] = field(
        default_factory=list
    )

    experience_required: str | None = None

    education_required: list[str] = field(
        default_factory=list
    )

    responsibilities: list[str] = field(
        default_factory=list
    )

    qualifications: list[str] = field(
        default_factory=list
    )

    location: str | None = None

    employment_type: str | None = None

    raw_text: str = ""

    missing_information: list[str] = field(
        default_factory=list
    )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class JobDescriptionProcessingAgent:
    """
    Job Description Processing Agent.

    Converts raw job description text into
    structured recruitment requirements.
    """

    KNOWN_SKILLS = [
        "Python",
        "Java",
        "C",
        "C++",
        "C#",
        "JavaScript",
        "TypeScript",
        "HTML",
        "CSS",
        "React",
        "Angular",
        "Vue",
        "FastAPI",
        "Django",
        "Flask",
        "Spring Boot",
        "SQL",
        "PostgreSQL",
        "MySQL",
        "MongoDB",
        "Redis",
        "Docker",
        "Kubernetes",
        "AWS",
        "Azure",
        "GCP",
        "Git",
        "GitHub",
        "Machine Learning",
        "Deep Learning",
        "Artificial Intelligence",
        "Generative AI",
        "Natural Language Processing",
        "Computer Vision",
        "TensorFlow",
        "PyTorch",
        "scikit-learn",
        "Pandas",
        "NumPy",
        "OpenCV",
        "LangChain",
        "LangGraph",
        "RAG",
        "Qdrant",
        "pgvector",
        "Celery",
        "Redis",
        "WebSockets",
        "REST API",
        "GraphQL",
        "Linux",
        "Jira",
        "Postman",
        "Selenium",
        "GitLab",
        "CI/CD",
        "Terraform",
        "Ansible",
    ]

    SECTION_ALIASES = {
        "responsibilities": [
            "responsibilities",
            "roles and responsibilities",
            "job responsibilities",
            "what you will do",
            "what you'll do",
            "key responsibilities",
            "duties",
        ],
        "required_skills": [
            "required skills",
            "required qualifications",
            "technical skills",
            "requirements",
            "must have",
            "must-have",
            "essential skills",
        ],
        "preferred_skills": [
            "preferred skills",
            "preferred qualifications",
            "nice to have",
            "nice-to-have",
            "desired skills",
            "good to have",
        ],
        "qualifications": [
            "qualifications",
            "basic qualifications",
            "minimum qualifications",
            "eligibility",
        ],
        "education": [
            "education",
            "educational qualification",
            "academic qualification",
            "academic requirements",
        ],
    }

    def process(
        self,
        job_description_text: str,
    ) -> JobDescriptionProfile:
        """
        Process raw job description text.
        """

        cleaned_text = self._clean_text(
            job_description_text
        )

        profile = JobDescriptionProfile(
            raw_text=cleaned_text
        )

        profile.job_title = (
            self._extract_job_title(cleaned_text)
        )

        profile.company = (
            self._extract_company(cleaned_text)
        )

        profile.location = (
            self._extract_location(cleaned_text)
        )

        profile.employment_type = (
            self._extract_employment_type(
                cleaned_text
            )
        )

        profile.required_skills = (
            self._extract_required_skills(
                cleaned_text
            )
        )

        profile.preferred_skills = (
            self._extract_preferred_skills(
                cleaned_text
            )
        )

        profile.experience_required = (
            self._extract_experience(
                cleaned_text
            )
        )

        profile.education_required = (
            self._extract_education(
                cleaned_text
            )
        )

        profile.responsibilities = (
            self._extract_section(
                cleaned_text,
                "responsibilities",
            )
        )

        profile.qualifications = (
            self._extract_section(
                cleaned_text,
                "qualifications",
            )
        )

        profile.missing_information = (
            self._find_missing_information(
                profile
            )
        )

        return profile

    def _clean_text(
        self,
        text: str,
    ) -> str:

        lines = []

        for line in text.splitlines():

            cleaned_line = " ".join(
                line.split()
            )

            if cleaned_line:
                lines.append(cleaned_line)

        return "\n".join(lines)

    def _extract_job_title(
        self,
        text: str,
    ) -> str | None:

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        title_keywords = [
            "software engineer",
            "software developer",
            "python developer",
            "backend developer",
            "frontend developer",
            "full stack developer",
            "data scientist",
            "machine learning engineer",
            "ai engineer",
            "ai developer",
            "devops engineer",
            "cloud engineer",
            "data analyst",
            "cyber security",
            "cybersecurity",
            "web developer",
        ]

        for line in lines[:15]:

            normalized = line.lower()

            for keyword in title_keywords:

                if keyword in normalized:

                    return line

        return None

    def _extract_company(
        self,
        text: str,
    ) -> str | None:

        patterns = [
            r"(?:company|organization|employer)\s*[:\-]\s*(.+)",
            r"(?:at|@)\s+([A-Z][A-Za-z0-9&.\- ]+)",
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                flags=re.IGNORECASE,
            )

            if match:

                return match.group(1).strip()

        return None

    def _extract_location(
        self,
        text: str,
    ) -> str | None:

        patterns = [
            r"(?:location|based in|work location)\s*[:\-]\s*(.+)",
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                flags=re.IGNORECASE,
            )

            if match:

                return match.group(1).strip()

        return None

    def _extract_employment_type(
        self,
        text: str,
    ) -> str | None:

        employment_types = [
            "full-time",
            "full time",
            "part-time",
            "part time",
            "contract",
            "internship",
            "intern",
            "temporary",
            "permanent",
        ]

        text_lower = text.lower()

        for employment_type in employment_types:

            if employment_type in text_lower:

                return employment_type

        return None

    def _extract_required_skills(
        self,
        text: str,
    ) -> list[str]:

        detected = []

        text_lower = text.lower()

        for skill in self.KNOWN_SKILLS:

            if skill.lower() in text_lower:

                if skill not in detected:

                    detected.append(skill)

        return detected

    def _extract_preferred_skills(
        self,
        text: str,
    ) -> list[str]:

        preferred_section = self._extract_section(
            text,
            "preferred_skills",
        )

        if not preferred_section:

            return []

        section_text = "\n".join(
            preferred_section
        )

        detected = []

        text_lower = section_text.lower()

        for skill in self.KNOWN_SKILLS:

            if skill.lower() in text_lower:

                if skill not in detected:

                    detected.append(skill)

        return detected

    def _extract_experience(
        self,
        text: str,
    ) -> str | None:

        patterns = [
            r"(\d+\+?\s*(?:years?|yrs?)"
            r"(?:\s+of)?\s+experience)",

            r"(\d+\s*-\s*\d+\s*(?:years?|yrs?)"
            r"(?:\s+of)?\s+experience)",
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                flags=re.IGNORECASE,
            )

            if match:

                return match.group(1).strip()

        return None

    def _extract_education(
        self,
        text: str,
    ) -> list[str]:

        education_keywords = [
            "b.tech",
            "b.e",
            "bachelor",
            "b.sc",
            "bca",
            "m.tech",
            "m.e",
            "master",
            "m.sc",
            "mca",
            "phd",
            "computer science",
            "information technology",
            "engineering",
        ]

        detected = []

        text_lower = text.lower()

        for keyword in education_keywords:

            if keyword in text_lower:

                if keyword not in detected:

                    detected.append(keyword)

        return detected

    def _extract_section(
        self,
        text: str,
        section_name: str,
    ) -> list[str]:

        aliases = self.SECTION_ALIASES.get(
            section_name,
            [section_name],
        )

        lines = text.splitlines()

        collected = []

        collecting = False

        all_aliases = [
            alias.lower()
            for values in self.SECTION_ALIASES.values()
            for alias in values
        ]

        for line in lines:

            cleaned = line.strip()

            if not cleaned:
                continue

            normalized = (
                cleaned.lower()
                .strip(":")
                .strip()
            )

            current_section = any(
                normalized == alias
                or normalized.startswith(
                    alias + ":"
                )
                for alias in aliases
            )

            if current_section:

                collecting = True

                continue

            if collecting:

                next_section = any(
                    normalized == alias
                    or normalized.startswith(
                        alias + ":"
                    )
                    for alias in all_aliases
                )

                if next_section:

                    break

                collected.append(
                    cleaned
                )

        return collected[:30]

    def _find_missing_information(
        self,
        profile: JobDescriptionProfile,
    ) -> list[str]:

        missing = []

        if not profile.job_title:

            missing.append(
                "job title"
            )

        if not profile.required_skills:

            missing.append(
                "required skills"
            )

        if not profile.experience_required:

            missing.append(
                "experience requirement"
            )

        if not profile.education_required:

            missing.append(
                "education requirement"
            )

        if not profile.responsibilities:

            missing.append(
                "responsibilities"
            )

        return missing
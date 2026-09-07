import re
from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class ResumeProfile:
    """
    Structured representation of a candidate resume.
    """

    name: str | None = None
    email: str | None = None
    phone: str | None = None

    skills: list[str] = field(default_factory=list)
    education: list[str] = field(default_factory=list)
    experience: list[str] = field(default_factory=list)
    projects: list[str] = field(default_factory=list)
    certifications: list[str] = field(default_factory=list)

    raw_text: str = ""

    missing_information: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class ResumeProcessingAgent:
    """
    Resume Processing Agent.

    Converts resume text into structured candidate information.
    """

    SECTION_ALIASES = {
        "education": [
            "education",
            "academic background",
            "academic qualification",
            "qualifications",
        ],
        "experience": [
            "experience",
            "work experience",
            "professional experience",
            "employment history",
        ],
        "projects": [
            "projects",
            "project experience",
            "academic projects",
            "personal projects",
        ],
        "certifications": [
            "certifications",
            "certification",
            "courses",
            "training",
        ],
        "skills": [
            "skills",
            "technical skills",
            "core skills",
            "key skills",
            "technologies",
        ],
    }

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
        "WebSockets",
        "REST API",
        "GraphQL",
        "Linux",
        "Jira",
    ]

    def process(self, resume_text: str) -> ResumeProfile:
        cleaned_text = self._clean_text(resume_text)

        profile = ResumeProfile(
            raw_text=cleaned_text
        )

        profile.name = self._extract_name(cleaned_text)
        profile.email = self._extract_email(cleaned_text)
        profile.phone = self._extract_phone(cleaned_text)

        profile.skills = self._extract_skills(cleaned_text)

        profile.education = self._extract_section(
            cleaned_text,
            "education",
        )

        profile.experience = self._extract_section(
            cleaned_text,
            "experience",
        )

        profile.projects = self._extract_section(
            cleaned_text,
            "projects",
        )

        profile.certifications = self._extract_section(
            cleaned_text,
            "certifications",
        )

        profile.missing_information = (
            self._find_missing_information(profile)
        )

        return profile

    def _clean_text(self, text: str) -> str:
        lines = []

        for line in text.splitlines():
            cleaned_line = " ".join(line.split())

            if cleaned_line:
                lines.append(cleaned_line)

        return "\n".join(lines)

    def _extract_name(self, text: str) -> str | None:
        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        if not lines:
            return None

        ignored = {
            "resume",
            "curriculum vitae",
            "cv",
            "profile",
        }

        for line in lines[:5]:
            normalized = line.lower()

            if normalized not in ignored:
                if "@" not in line and not re.search(
                    r"\d{7,}",
                    line,
                ):
                    return line

        return None

    def _extract_email(self, text: str) -> str | None:
        pattern = (
            r"[A-Za-z0-9._%+-]+"
            r"@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
        )

        match = re.search(pattern, text)

        return match.group(0) if match else None

    def _extract_phone(self, text: str) -> str | None:
        patterns = [
            r"(?:\+91[\s-]?)?[6-9]\d{9}",
            r"\+?\d[\d\s().-]{8,}\d",
        ]

        for pattern in patterns:
            match = re.search(pattern, text)

            if match:
                return match.group(0).strip()

        return None

    def _extract_skills(self, text: str) -> list[str]:
        detected = []
        text_lower = text.lower()

        for skill in self.KNOWN_SKILLS:
            if skill.lower() in text_lower:
                detected.append(skill)

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

        all_section_aliases = [
            alias.lower()
            for values in self.SECTION_ALIASES.values()
            for alias in values
        ]

        for line in lines:
            cleaned = line.strip()

            if not cleaned:
                continue

            normalized = cleaned.lower().strip(":").strip()

            is_current_section = any(
                normalized == alias
                or normalized.startswith(alias + ":")
                for alias in aliases
            )

            if is_current_section:
                collecting = True
                continue

            if collecting:
                is_next_section = any(
                    normalized == alias
                    or normalized.startswith(alias + ":")
                    for alias in all_section_aliases
                )

                if is_next_section:
                    break

                collected.append(cleaned)

        return collected[:20]

    def _find_missing_information(
        self,
        profile: ResumeProfile,
    ) -> list[str]:

        missing = []

        if not profile.name:
            missing.append("name")

        if not profile.email:
            missing.append("email")

        if not profile.phone:
            missing.append("phone")

        if not profile.skills:
            missing.append("skills")

        if not profile.education:
            missing.append("education")

        if not profile.experience:
            missing.append("experience")

        if not profile.projects:
            missing.append("projects")

        return missing
from pydantic import BaseModel, ConfigDict, Field


class EducationItem(BaseModel):
    degree: str | None = None
    institution: str | None = None
    graduation_year: int | None = None


class ExperienceItem(BaseModel):
    company: str | None = None
    role: str | None = None
    duration: str | None = None
    responsibilities: list[str] = Field(
        default_factory=list
    )


class ProjectItem(BaseModel):
    name: str | None = None
    description: str | None = None
    technologies: list[str] = Field(
        default_factory=list
    )


class ResumeProfileSchema(BaseModel):
    """
    Validated structured candidate resume profile.
    """

    model_config = ConfigDict(
        extra="ignore"
    )

    name: str | None = None

    email: str | None = None

    phone: str | None = None

    skills: list[str] = Field(
        default_factory=list
    )

    education: list[EducationItem] = Field(
        default_factory=list
    )

    experience: list[ExperienceItem] = Field(
        default_factory=list
    )

    projects: list[ProjectItem] = Field(
        default_factory=list
    )

    certifications: list[str] = Field(
        default_factory=list
    )

    summary: str | None = None

    total_experience_years: float | None = Field(
        default=None,
        ge=0,
    )

    missing_information: list[str] = Field(
        default_factory=list
    )
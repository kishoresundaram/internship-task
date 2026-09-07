from datetime import datetime

from sqlalchemy import DateTime, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class JobDescription(Base):
    __tablename__ = "job_descriptions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    job_title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    company: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    required_skills: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    preferred_skills: Mapped[list | None] = mapped_column(
        JSON,
        nullable=True,
    )

    experience_required: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    education_required: Mapped[list | None] = mapped_column(
        JSON,
        nullable=True,
    )

    responsibilities: Mapped[list | None] = mapped_column(
        JSON,
        nullable=True,
    )

    qualifications: Mapped[list | None] = mapped_column(
        JSON,
        nullable=True,
    )

    location: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
    )

    employment_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    structured_profile: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
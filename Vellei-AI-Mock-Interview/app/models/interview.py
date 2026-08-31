from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class InterviewSession(Base):
    __tablename__ = "interview_sessions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    candidate_id = Column(
        Integer,
        ForeignKey("candidates.id"),
        nullable=False
    )

    job_id = Column(
        Integer,
        ForeignKey("jobs.id"),
        nullable=True
    )

    job_title = Column(
        String,
        nullable=False
    )

    difficulty = Column(
        String,
        default="medium"
    )

    status = Column(
        String,
        default="started"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    candidate = relationship(
        "Candidate",
        back_populates="interviews"
    )

    questions = relationship(
        "Question",
        back_populates="interview",
        cascade="all, delete-orphan"
    )


# Compatibility with existing routes
Interview = InterviewSession
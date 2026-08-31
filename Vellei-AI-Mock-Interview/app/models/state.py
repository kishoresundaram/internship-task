from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func

from app.database import Base


class InterviewState(Base):
    __tablename__ = "interview_states"

    id = Column(Integer, primary_key=True, index=True)

    interview_id = Column(
        Integer,
        ForeignKey("interview_sessions.id"),
        nullable=False,
        unique=True
    )

    current_competency = Column(String(150), nullable=True)
    competencies_covered = Column(Text, nullable=True)
    competencies_remaining = Column(Text, nullable=True)

    strengths = Column(Text, nullable=True)
    weaknesses = Column(Text, nullable=True)

    current_difficulty = Column(String(50), default="medium")

    state_json = Column(Text, nullable=True)

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

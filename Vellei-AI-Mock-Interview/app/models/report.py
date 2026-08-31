from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.database import Base


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)

    candidate_id = Column(
        Integer,
        ForeignKey("candidates.id"),
        nullable=False
    )

    overall_score = Column(
        Float,
        default=0.0
    )

    strengths = Column(
        Text,
        nullable=True
    )

    weaknesses = Column(
        Text,
        nullable=True
    )

    recommendations = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    candidate = relationship(
        "Candidate"
    )
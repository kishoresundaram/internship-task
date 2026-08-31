from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.database import Base


class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True, index=True)

    answer_id = Column(
        Integer,
        ForeignKey("answers.id"),
        nullable=False,
        unique=True
    )

    score = Column(Float, default=0.0)

    technical_score = Column(
        Float,
        default=0.0
    )

    communication_score = Column(
        Float,
        default=0.0
    )

    relevance_score = Column(
        Float,
        default=0.0
    )

    feedback = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    answer = relationship(
        "Answer",
        back_populates="evaluation"
    )
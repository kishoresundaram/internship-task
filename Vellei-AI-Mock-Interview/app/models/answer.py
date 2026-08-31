from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.database import Base


class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)

    question_id = Column(
        Integer,
        ForeignKey("questions.id"),
        nullable=False
    )

    answer_text = Column(Text, nullable=False)

    score = Column(Float, nullable=True)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    question = relationship(
        "Question",
        back_populates="answers"
    )

    evaluation = relationship(
        "Evaluation",
        back_populates="answer",
        uselist=False,
        cascade="all, delete-orphan"
    )
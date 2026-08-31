from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)

    session_id = Column(
        Integer,
        ForeignKey("interview_sessions.id"),
        nullable=False
    )

    question_text = Column(Text, nullable=False)
    difficulty = Column(String, default="medium")
    question_type = Column(String, default="technical")

    interview = relationship(
        "InterviewSession",
        back_populates="questions"
    )

    answers = relationship(
        "Answer",
        back_populates="question",
        cascade="all, delete-orphan"
    )
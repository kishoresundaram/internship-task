from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func

from app.database import Base


class LearningRecommendation(Base):
    __tablename__ = "learning_recommendations"

    id = Column(Integer, primary_key=True, index=True)

    interview_id = Column(
        Integer,
        ForeignKey("interview_sessions.id"),
        nullable=False
    )

    skill = Column(String(150), nullable=False)
    priority = Column(String(50), default="medium")
    recommendation = Column(Text, nullable=False)
    learning_action = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

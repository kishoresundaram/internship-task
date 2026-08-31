from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime
from sqlalchemy.sql import func

from app.database import Base


class SkillGap(Base):
    __tablename__ = "skill_gaps"

    id = Column(Integer, primary_key=True, index=True)

    interview_id = Column(
        Integer,
        ForeignKey("interview_sessions.id"),
        nullable=False
    )

    skill = Column(String(150), nullable=False)
    expected_level = Column(String(50), nullable=True)
    demonstrated_level = Column(String(50), nullable=True)

    gap_score = Column(Float, default=0)

    evidence = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

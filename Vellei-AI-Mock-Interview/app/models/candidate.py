from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    phone = Column(String, nullable=True)
    resume_text = Column(Text, nullable=True)

    interviews = relationship(
        "InterviewSession",
        back_populates="candidate",
        cascade="all, delete-orphan"
    )
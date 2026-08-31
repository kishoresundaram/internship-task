from sqlalchemy import Column, Integer, String, Text

from app.db.database import Base


class JobDescription(Base):
    __tablename__ = "job_descriptions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    filename = Column(
        String,
        nullable=False
    )

    file_path = Column(
        String,
        nullable=False
    )

    extracted_text = Column(
        Text,
        nullable=False
    )
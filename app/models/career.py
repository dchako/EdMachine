from sqlalchemy import Column, Text, String
from app.models.base import BaseModel
from sqlalchemy.orm import relationship


class CareerModel(BaseModel):
    """Model for analysis career."""

    __tablename__ = "career"

    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)

    course = relationship("CourseModel", lazy="joined", secondary="career_course")

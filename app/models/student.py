from sqlalchemy import Column, String
from app.models.base import BaseModel
from sqlalchemy.orm import relationship


class StudentModel(BaseModel):
    """Model for analysis student."""

    __tablename__ = "student"

    full_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    adress = Column(String(300), nullable=False)
    telephone = Column(String(100), nullable=False)

    course = relationship("CourseModel", lazy="joined", secondary="CareerCourseModel")

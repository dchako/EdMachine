from sqlalchemy import Column, ForeignKey, String
from app.models.base import BaseModel


class CareerCourseModel(BaseModel):
    """Model for analysis career and course."""

    __tablename__ = "career_course"

    career_id = Column(String(36), ForeignKey("career.id"))
    course_id = Column(String(36), ForeignKey("course.id"))

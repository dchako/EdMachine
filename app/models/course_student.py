from sqlalchemy import Column, ForeignKey, String
from app.models.base import BaseModel


class CourseStudentModel(BaseModel):
    """Model for analysis course and student."""

    __tablename__ = "course_student"

    student_id = Column(String(36), ForeignKey("student.id"))
    course_id = Column(String(36), ForeignKey("course.id"))

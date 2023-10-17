from sqlalchemy import Column, Text, String
from app.models.base import BaseModel


class CourseModel(BaseModel):
    """Model for analysis course."""

    __tablename__ = "course"

    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)

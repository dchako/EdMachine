from app.models.course import CourseModel
from app.repos.base import BaseRepo


class CourseRepo(BaseRepo):
    """Class to manage Course Repository."""

    _model = CourseModel

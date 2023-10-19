from app.repos.course import CourseRepo
from app.services.base import BaseService


class CourseService(BaseService):
    """Class to manage Course Service."""

    _repo = CourseRepo

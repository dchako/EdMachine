from app.repos.course import CourseRepo
from app.services.base import BaseService


class CourseService(BaseService):
    """Class to manage Course Service."""

    _repo = CourseRepo

    @classmethod
    def create(cls, payload):
        """Creates a request."""

        request = super().create(payload)
        cls.logger.info(f"Request {request.id} created")
        return request

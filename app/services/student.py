from app.repos.student import StudentRepo
from app.services.base import BaseService


class StudentService(BaseService):
    """Class to Student Service."""

    _repo = StudentRepo

    @classmethod
    def create(cls, payload):
        """Creates a request."""

        request = super().create(payload)
        cls.logger.info(f"Request {request.id} created")
        return request

    @classmethod
    def get_many_paginated(cls, filters):
        """Get many paginated."""

        cls.logger.info(f"Student Get Many Paginated Request with filters: [{filters}]")

        return cls._repo.get_many_by_pagination(filters)

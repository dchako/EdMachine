from app.repos.career import CareerRepo
from app.services.base import BaseService


class CareerService(BaseService):
    """Class to career Service."""

    _repo = CareerRepo

    @classmethod
    def create(cls, payload):
        """Creates a request."""

        request = super().create(payload)
        cls.logger.info(f"Request {request.id} created")
        return request

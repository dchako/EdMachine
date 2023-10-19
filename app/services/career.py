from app.repos.career import CareerRepo
from app.services.base import BaseService


class CareerService(BaseService):
    """Class to career Service."""

    _repo = CareerRepo

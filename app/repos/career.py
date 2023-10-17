from app.models.career import CareerModel
from app.repos.base import BaseRepo


class CareerRepo(BaseRepo):
    """Class to manage Career Repository."""

    _model = CareerModel

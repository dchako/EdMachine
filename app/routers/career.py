from fastapi import APIRouter
from app.logger import Logger
from app.schemas.career import careerResponseAllSchema, careerResponseSchema
from app.schemas.career import careerSchema
from app.services.career import CareerService

logger = Logger.get_logger()

career_router = APIRouter()


@career_router.post("", response_model=careerResponseSchema)
def create_edmachine_request(payload: careerSchema):
    """Creates a Career requests."""

    payload = payload.dict()
    return CareerService.create(payload)


@career_router.get("", response_model=careerResponseAllSchema)
def get_all_careers():
    """Retrieves all Career requests by filters."""

    return CareerService.get_all()


@career_router.get("/{id}", response_model=careerResponseSchema)
def get_one_edmachine_request(id: str):
    """Retrieves a Career request."""

    return CareerService.get_one(id)

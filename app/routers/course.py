from fastapi import APIRouter

from app.logger import Logger
from app.schemas.course import courseResponseAllSchema, courseResponseSchema
from app.schemas.course import courseSchema
from app.services.course import CourseService

logger = Logger.get_logger()

course_router = APIRouter()


@course_router.post("", response_model=courseResponseSchema)
def create_course(payload: courseSchema):
    """Creates a course requests."""

    payload = payload.dict()
    return CourseService.create(payload)


@course_router.get("", response_model=courseResponseAllSchema)
def get_all_courses():
    """Retrieves all course requests by filters."""

    return CourseService.get_all()


@course_router.get("/{id}", response_model=courseResponseSchema)
def get_one_course_request(id: str):
    """Retrieves a course request."""

    return CourseService.get_one(id)

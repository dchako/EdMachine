from fastapi import APIRouter
from fastapi import Depends
from fastapi import Response

from app.logger import Logger
from app.schemas.student import studentResponseSchema
from app.schemas.student import studentGetAllRequestSchema, studentResponseAllSchema
from app.schemas.student import studentRequestCreateSchema 
from app.services.student import StudentService

logger = Logger.get_logger()

student_router = APIRouter()


@student_router.post("", response_model=studentResponseSchema)
def create_student(payload: studentRequestCreateSchema):
    """Creates student requests."""

    payload = payload.dict()
    return StudentService.create(payload)


@student_router.get("", response_model=studentResponseAllSchema)
def get_many_students(response: Response, params: studentGetAllRequestSchema = Depends()):
    """Retrieves many student requests by filters."""

    filters = params.format(params)
    students, pagination_info = StudentService.get_many_paginated(filters)
    response.headers.update(pagination_info)
    return students


@student_router.get("/{id}", response_model=studentResponseSchema)
def get_one_edmachine_request(id: str):
    """Retrieves a student request."""

    return StudentService.get_one(id)

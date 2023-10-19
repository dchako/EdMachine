from typing import Optional, List
from app.schemas.base import BaseSchema
from app.schemas.base import BaseResponseSchema
from app.schemas.course import courseSchema


class studentSchema(BaseSchema):
    """student Schema.
        {
        "full_name": "string",
        "email": "string",
        "adress": "string",
        "telephone": "string",
        "courses": [
            {
            "course_id": "string"
            }
        ]
        }
    """

    full_name: str
    email: str
    adress: str
    telephone: str
    id: Optional[str]


class studentRequestCreateSchema(studentSchema):
    """student Request Create Schema."""

    courses: Optional[List[courseSchema]]


class studentResponseSchema(BaseResponseSchema):
    """student Response Schema."""

    data: studentSchema


class studentResponseAllSchema(BaseResponseSchema):
    """student Response Schema all."""

    data: Optional[List[studentSchema]]


class studentGetAllRequestSchema(BaseSchema):
    """student get all schema"""

    page: Optional[int]
    page_size: Optional[int]

    @classmethod
    def format(cls, values):
        """Format student Get All Request Schema ."""

        filters = values.dict(exclude_none=True)
        if filters.get("page"):
            filters['pagination'] = {
                'page_number': filters.pop('page', 1),
                'page_size': filters.pop('page_size', 10)
            }

        return filters

from typing import Optional, List
from app.schemas.base import BaseSchema
from app.schemas.base import BaseResponseSchema


class courseSchema(BaseSchema):
    """course Schema."""

    name: str
    description: str


class courseResponseSchema(BaseResponseSchema):
    """course Response Schema."""

    data: courseSchema


class courseResponseAllSchema(BaseResponseSchema):
    """course Response Schema all."""

    data: Optional[List[courseSchema]]


class courseGetAllRequestSchema(BaseSchema):
    """course get all schema"""

    page: Optional[int]
    page_size: Optional[int]

    @classmethod
    def format(cls, values):
        """Format course Get All Request Schema ."""

        filters = values.dict(exclude_none=True)
        if filters.get("page"):
            filters['pagination'] = {
                'page_number': filters.pop('page', 1),
                'page_size': filters.pop('page_size', 10)
            }

        return filters

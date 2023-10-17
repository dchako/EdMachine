from typing import Optional, List
from app.schemas.base import BaseSchema
from app.schemas.base import BaseResponseSchema


class careerSchema(BaseSchema):
    """career Schema."""

    name: str
    description: str


class careerResponseSchema(BaseResponseSchema):
    """career Response Schema."""

    data: careerSchema


class careerResponseAllSchema(BaseResponseSchema):
    """career Response Schema all."""

    data: Optional[List[careerSchema]]


class careerGetAllRequestSchema(BaseSchema):
    """Career get all schema"""

    page: Optional[int]
    page_size: Optional[int]

    @classmethod
    def format(cls, values):
        """Format career Get All Request Schema ."""

        filters = values.dict(exclude_none=True)
        if filters.get("page"):
            filters['pagination'] = {
                'page_number': filters.pop('page', 1),
                'page_size': filters.pop('page_size', 10)
            }

        return filters

from app.database import get_session
from sqlalchemy.sql.expression import not_
from app.models.student import StudentModel
from app.repos.base import BaseRepo
import math


class StudentRepo(BaseRepo):
    """Class to manage Student Repository."""

    _model = StudentModel

    @classmethod
    def _get_pagination_info(cls, page, page_size, total):
        """Retrieves pagination info."""

        return {
            'X-Total-Count': str(total),
            'X-Per-Page': str(page_size),
            'X-Current-Page': str(page),
            'X-Item-Range-From': str(((page * page_size) - page_size) + 1),
            'X-Item-Range-To': str(page * page_size),
            'X-Total-Pages': str(int(math.ceil(total / float(page_size)))),
        }

    @classmethod
    def get_all(cls):
        """Retrieves all Students."""

        with get_session() as session:
            Students = session.query(cls._model).all()
        return Students

    @classmethod
    def add_course(cls, student, courses):
        """Add course to student."""

        with get_session() as session:
            for course in courses:
                student.courses.append(course)
            session.add(student)
            session.commit()
        return student

    @classmethod
    def get_many_by_pagination(cls, filters):
        """Retrieve many Students by filters."""

        order = filters.pop('order_by', 'created_at')
        page_number = filters.pop('page_number', None)
        page_size = filters.pop('page_size', 10)
        filter_name = filters.pop('name', None)

        with get_session() as session:
            query = session.query(cls._model.id, cls._model.full_name, cls._model.email, cls._model.adress, cls._model.telephone)

            if order:
                if order[0] == "-":
                    order = order[1:]
                    model_attribute = getattr(cls._model, order)
                    order_query = model_attribute.desc()
                else:
                    model_attribute = getattr(cls._model, order)
                    order_query = model_attribute.asc()
                query = query.order_by(order_query)

            if page_number is None:
                query = query.all()
                page_size = len(query) or 1
                return query, cls._get_pagination_info(1, page_size, page_size)

            if filter_name is not None:
                filter_value = filter_name.split(':')
                filter_name = "name"
                operator = None
                if len(filter_value) > 1:
                    operator = filter_value[0]
                    filter_value = filter_value[1]

                if operator == 'contains':
                    query = query.filter(getattr(cls._model, filter_name).contains(filter_value))
                elif operator == 'ends':
                    query = query.filter(getattr(cls._model, filter_name).endswith(filter_value))
                elif operator == 'not':
                    query = query.filter(not_(getattr(cls._model, filter_name).contains(filter_value)))
                elif operator == 'starts':
                    query = query.filter(getattr(cls._model, filter_name).startswith(filter_value))
                else:
                    query = query.filter(getattr(cls._model, filter_name) == filter_value)

            query = query.filter(cls._model.deleted_at.is_(None)).filter_by(**filters)

            if page_number <= 0:
                raise AttributeError('page needs to be >= 1')
            if page_size <= 0:
                query = query.all()
                page_size = len(query) or 1
                return query, cls._get_pagination_info(1, page_size, page_size)

        Students = query.limit(page_size).offset((page_number - 1) * page_size).all()

        return Students, cls._get_pagination_info(page_number, page_size, query.order_by(None).count())

from app.repos.student import StudentRepo
from app.services.course import CourseService
from app.services.base import BaseService
from app.exceptions import ResourceNotFoundError


class StudentService(BaseService):
    """Class to Student Service."""

    _repo = StudentRepo

    @classmethod
    def add_course(cls, student_id, courses):
        """Add course to student."""

        student = cls.get_one(id=student_id)
        course = [
            CourseService.get_one(id=course['course_id'])
            for course in courses
        ]
        student = cls._repo.add_course(student, course)
        return student

    @classmethod
    def create(cls, payload):
        """Creates a students."""

        student = cls._repo.create({
            "full_name": payload["full_name"],
            "email": payload["email"],
            "adress": payload["adress"],
            "telephone": payload["telephone"]
        })

        for course in payload.pop("courses", []):
            if not (course := CourseService._repo.get_one_by_filters({"name": course["name"]})):
                raise ResourceNotFoundError(resource=course)
                # course = CourseService.create(course)
            cls.add_course(student.id, [{"course_id": course.id}])

        return cls.get_one(student.id)

    @classmethod
    def get_many_paginated(cls, filters):
        """Get many paginated."""

        cls.logger.info(f"Student Get Many Paginated Request with filters: [{filters}]")

        return cls._repo.get_many_by_pagination(filters)

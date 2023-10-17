from app.exceptions import ResourceNotFoundError
from app.logger import Logger


class BaseService:
    """Class to manage Base Service."""

    _repo = None
    logger = Logger.get_logger()

    @classmethod
    def get_one(cls, id):
        """Retrieves a resource by id."""

        resource = cls._repo.get_one(id)
        if not resource:
            cls.logger.info(f'Not found id get one {id}')
            raise ResourceNotFoundError(resource=id)
        return resource

    @classmethod
    def get_one_by_filters(cls, filters):
        """Retrieves many resources."""

        if resource := cls._repo.get_one_by_filters(filters):
            return resource
        else:
            raise ResourceNotFoundError(resource=filters)

    @classmethod
    def get_many(cls, filters):
        """Retrieves many resources."""

        return cls._repo.get_many(filters)

    @classmethod
    def get_all(cls):
        """Retrieves all resources."""

        return cls._repo.get_all()

    @classmethod
    def create(cls, payload):
        """Creates a resources."""

        return cls._repo.create(payload)

    @classmethod
    def create_many(cls, payload):
        """Creates many resources."""

        return cls._repo.create_many(payload)

    @classmethod
    def update(cls, id, payload):
        """Change data a resources."""

        cls.get_one(id)
        return cls._repo.update(id, payload)

    @classmethod
    def delete(cls, id):
        """Delete data a resources."""

        return cls._repo.delete(id)

    @classmethod
    def delete_by_filters(cls, filters):
        """Deleted all by filters."""

        return cls._repo.delete_by_filters(filters)

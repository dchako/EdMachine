import datetime
from app.database import get_session
from app.logger import Logger
import math


class BaseRepo:
    """Class to manage Base Repository."""

    _model = None
    logger = Logger.get_logger()

    @classmethod
    def get_one(cls, id):
        """Retrieve a resource by id."""
        with get_session() as session:
            session.flush()
            resource = session.query(cls._model).filter(cls._model.deleted_at.is_(None)).filter_by(id=id).first()
        return resource

    @classmethod
    def get_one_by_filters(cls, filters):
        """Retrieve a resource by filters."""
        with get_session() as session:
            session.flush()
            resource = session.query(cls._model).filter(cls._model.deleted_at.is_(None)).filter_by(**filters).first()
        return resource

    @classmethod
    def get_many(cls, filters):
        """Retrieve many resources by filters."""
        with get_session() as session:
            session.flush()
            resources = session.query(cls._model).filter(cls._model.deleted_at.is_(None)).filter_by(**filters).all()
        return resources

    @classmethod
    def get_all(cls):
        """Retrieves all resources."""
        with get_session() as session:
            session.flush()
            resources = session.query(cls._model).filter(cls._model.deleted_at.is_(None)).all()
        return resources

    @classmethod
    def create(cls, payload):
        """Creates a resource."""
        with get_session() as session:
            resource = cls._model(**payload)
            session.add(resource)
            session.commit()
            session.refresh(resource)
            cls.logger.info(f"{cls._model} {resource.id} created")
        return resource

    @classmethod
    def create_many(cls, payloads):
        """Creates many resources."""
        with get_session() as session:
            resources = [cls._model(**payload) for payload in payloads]
            session.bulk_save_objects(resources, return_defaults=True)
            session.commit()
            session.flush()
            cls.logger.info(f"{len(resources)} resources created")
        return resources

    @classmethod
    def create_many_batch(cls, payloads, batch=1000):
        """Creates many resources by batch."""

        with get_session() as session:
            total = 0
            end_payload = len(payloads)
            for start_batch in range(0, end_payload, batch):
                resources_batch = []
                end_batch = end_payload if ((start_batch + batch - 1) > end_payload) else (start_batch + batch)
                for payload in payloads[start_batch:end_batch]:
                    resources_batch.append(cls._model(**payload))
                    total += 1
                session.bulk_save_objects(resources_batch, return_defaults=True)
                session.commit()
                session.flush()
            cls.logger.info(f"{total} resources created")
        return True

    @classmethod
    def update(cls, id, payload):
        """Updates a resource."""
        with get_session() as session:
            session.query(cls._model).filter_by(id=id).filter(cls._model.deleted_at.is_(None)).update(payload)
            session.commit()
            session.flush()
        return cls.get_one(id)

    @classmethod
    def delete(cls, id):
        """Deleted a resource."""
        with get_session() as session:
            resource = session.query(cls._model).filter_by(id=id).update({'deleted_at': datetime.datetime.now()})
            session.commit()
            session.flush()
        return resource

    @classmethod
    def delete_by_filters(cls, filters):
        """Deleted all by filters."""
        with get_session() as session:
            resource = session.query(cls._model).filter_by(**filters).update({'deleted_at': datetime.datetime.now()})
            session.commit()
            session.flush()
        return resource

    @classmethod
    def _get_pagination_info(cls, page, page_size, total):
        """Retrieves pagination info."""

        return {
            'X-Total-Count': str(total),
            'X-Per-Page': str(page_size),
            'X-Current-Page': str(page),
            'X-Item-Range-From': str(((page * page_size) - page_size) + 1),
            'X-Item-Range-To': str(min(total, page * page_size)),
            'X-Total-Pages': str(int(math.ceil(total / float(page_size)))),
        }

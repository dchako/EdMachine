from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

from app.config import settings
from app.logger import Logger

logger = Logger.get_logger()


def get_engine(database_config: dict):

    return create_engine(**database_config)


def get_maker(database_config: dict):
    return sessionmaker(
        autocommit=False, 
        autoflush=True,
        expire_on_commit=False,
        bind=get_engine(database_config)
    )


s_session = scoped_session(get_maker(settings.DATABASE_CONFIG_DICT))


@contextmanager
def get_session():
    session = s_session()
    try:
        yield session
    except Exception as ex:
        logger.exception(ex)
        session.rollback()
        raise
    finally:
        session.close()

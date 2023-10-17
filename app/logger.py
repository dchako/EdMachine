import sys
import logging

from app.config import settings


class Logger:
    """Class to manage logger service."""

    def get_logger(name=settings.API_NAME, level=None, log_path=None, log_format=None):
        """Retrieves logger module."""

        try:
            if log_format is None:
                log_format = '%(asctime)s - %(levelname)s - %(pathname)s - Line: %(lineno)d - '
            if log_path is None:
                log_path = settings.PATCH_LOGS
            logger = logging.getLogger(name)
            formatter = logging.Formatter(fmt=f"{log_format} %(message)s")
            file_handler = logging.FileHandler(f'{log_path}/{name}.log')
            file_handler.setFormatter(formatter)
            handler = logging.StreamHandler(sys.stdout)
            logger.handlers = []
            logger.addHandler(file_handler)
            logger.addHandler(handler)
            if level is None:
                level = settings.LEVEL_LOGS
            logger.setLevel(level)
            logger.propagate = False
            return logger
        except Exception as ex:
            raise ex

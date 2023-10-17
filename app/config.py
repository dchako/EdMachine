from os import getenv, path, getcwd
from pydantic import BaseSettings


class BaseConfig(BaseSettings):
    """Class to manage api settings."""

    API_NAME: str = getenv('API_NAME', 'COMMONS')
    API_VERSION: str = "0.0.2"
    DB_HOST: str = getenv('DB_HOST')
    DB_PORT: int = getenv('DB_PORT')
    DB_NAME: str = getenv('DB_NAME')
    DB_USER: str = getenv('DB_USER')
    DB_PASS: str = getenv('DB_PASS')
    PATCH_LOGS: str = getenv('PATCH_LOGS', path.abspath(getcwd()))
    LEVEL_LOGS: str = getenv('LEVEL_LOGS', 'DEBUG')

    DATABASE_URI: str = f"mysql+mysqldb://{DB_USER}:{DB_PASS}" \
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8"
    DATABASE_CONFIG_DICT: dict = {
        "url": DATABASE_URI,
        "pool_use_lifo": True,
        "pool_pre_ping": True,
        "pool_recycle": 3600,
        "echo_pool": True
    }


settings = BaseConfig()

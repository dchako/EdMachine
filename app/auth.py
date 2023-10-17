import contextvars
import inspect
import types

from app.logger import Logger

logger = Logger.get_logger()
request_session = contextvars.ContextVar("session", default=types.SimpleNamespace())


def session():
    return request_session.get()


def authenticated(validate=[], reject=True, operator="AND"):
    """Validate if the user is authenticated."""

    # Validate if the user is authenticated
    def auth(func):
        def wrapper(*args, **kwargs):
            # Get request
            return func(*args, **kwargs)
        wrapper.__name__ = func.__name__
        wrapper.__signature__ = inspect.Signature(
            parameters=[
                *inspect.signature(func).parameters.values(),
                *filter(
                    lambda p: p.kind not in (
                        inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD),
                    inspect.signature(wrapper).parameters.values()
                ),
            ],
            return_annotation=inspect.signature(func).return_annotation
        )
        return wrapper
    return auth

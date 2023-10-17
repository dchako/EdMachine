from fastapi.exceptions import RequestValidationError

from app.exceptions import exception_middleware
from app.exceptions import validation_exception_handler
from app.session import session_middleware
from fastapi.middleware.cors import CORSMiddleware


def init_middlewares(app):
    """Init app middlewares."""

    app.exception_handler(RequestValidationError)(validation_exception_handler)
    app.middleware('http')(exception_middleware)
    app.middleware('http')(session_middleware)

    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"]
    )

import types
import fastapi

from app.auth import request_session


async def session_middleware(request: fastapi.Request, call_next):
    """Init session middlware."""

    initial_g = types.SimpleNamespace()
    request_session.set(initial_g)
    return await call_next(request)

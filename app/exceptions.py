from fastapi import status
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import sqlalchemy

from app.logger import Logger

logger = Logger.get_logger()


class ResourceNotFoundError(Exception):
    """Exception when DB resource not found."""

    msg = "resource {} not found"

    def __init__(self, resource):
        self.msg = self.msg.format(resource)


class RequestError(Exception):
    """Exception on error in request creation."""

    msg = "request error: {}"

    def __init__(self, error):
        self.msg = self.msg.format(error)


async def exception_middleware(request: Request, call_next):
    try:
        return await call_next(request)

    except sqlalchemy.exc.DatabaseError as ex:
        logger.exception(ex)
        return JSONResponse({
            'status': 'error', 
            'message': str(ex.orig)
        }, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except ResourceNotFoundError as ex:
        logger.exception(ex)
        return JSONResponse({
            'status': 'fail', 
            'data': ex.msg
        }, status_code=status.HTTP_404_NOT_FOUND)

    except Exception as ex:
        logger.exception(ex)
        return JSONResponse({
            'status': 'error',
            'data': 'Unexpected error. Try again later.'
        }, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """rewrite the class to format the output message."""

    error_msg = ''
    for error in exc.errors()[0]["loc"]:

        if (isinstance(error, int)):
            error = f"[{error}]"

        error_msg += f'{error}.'

    data = f'{exc.errors()[0]["msg"]} {error_msg[:-1]}'

    return JSONResponse({
        'status': 'fail',
        'data': data
    }, status_code=status.HTTP_400_BAD_REQUEST)

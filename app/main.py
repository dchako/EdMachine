from fastapi import FastAPI

from app.config import settings
from app.middleware import init_middlewares

from app.routers.student import student_router
from app.routers.career import career_router
from app.routers.course import course_router


def init_app():
    """Initialize app."""

    app = FastAPI(
        title=settings.API_NAME, 
        version=settings.API_VERSION
    )

    app.include_router(
        student_router,
        prefix="/student", 
        tags=["students"]
    )

    app.include_router(
        career_router,
        prefix="/career", 
        tags=["careers"]
    )

    app.include_router(
        course_router,
        prefix="/course", 
        tags=["courses"]
    )

    init_middlewares(app)

    return app


app = init_app()


@app.get("/")
def index():
    return {
        'api': {
            'name': settings.API_NAME, 
            'version': settings.API_VERSION
        }
    }

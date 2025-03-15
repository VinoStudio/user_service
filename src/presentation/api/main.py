from fastapi import FastAPI

from domain.base.exceptions.application import AppException
from presentation.api.user.handlers import user_router
from fastapi.responses import JSONResponse

from presentation.api.lifespan import lifespan
from presentation.api.exception_builder import configure_base_exception_handlers


def create_app() -> FastAPI:
    app = FastAPI(
        title="Simple Kafka Chat",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        description="Simple Kafka Chat API",
        debug=True,
        # lifespan=lifespan,
    )

    configure_base_exception_handlers(app)

    app.include_router(
        router=user_router,
        prefix="/user",
        tags=["User"],
    )
    return app

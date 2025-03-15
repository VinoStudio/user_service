from typing import Dict, Any

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from domain.base.exceptions.application import AppException
from domain.base.exceptions.domain import DomainException
from infrastructure.base.exception import InfrastructureException
from application.base.exception import ApplicationException
from infrastructure.exceptions import (
    DatabaseException,
    RepositoryException,
    UserIdAlreadyExistsErrorException,
    UserWithUsernameDoesNotExistException,
    UserIsDeletedException,
    UserDoesNotExistException,
)
from domain.base.exceptions.domain import ValidationException
from application.exceptions import UsernameAlreadyExistsException
from presentation.api.base_schemas import ErrorResponseSchema


def configure_base_exception_handlers(app: FastAPI):
    """Configure all exception handlers for the application"""

    @app.exception_handler(AppException)
    async def base_exception_handler(request, exc):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": {
                    "message": exc.message,
                    "type": exc.__class__.__name__,
                }
            },
        )

    @app.exception_handler(ApplicationException)
    async def application_exception_handler(request, exc):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": {
                    "message": exc.message,
                    "type": exc.__class__.__name__,
                }
            },
        )

    @app.exception_handler(DomainException)
    async def domain_exception_handler(request, exc):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": {
                    "message": exc.message,
                    "type": exc.__class__.__name__,
                }
            },
        )

    @app.exception_handler(InfrastructureException)
    @app.exception_handler(DatabaseException)
    async def infrastructure_exception_handler(request, exc):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": {"message": exc.message, "type": exc.__class__.__name__}},
        )

    @app.exception_handler(ValidationException)
    async def domain_validation_exception_handler(request, exc):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"error": {"message": exc.message, "type": exc.__class__.__name__}},
        )

    @app.exception_handler(UserDoesNotExistException)
    @app.exception_handler(UserWithUsernameDoesNotExistException)
    async def not_found_exception_handler(request, exc):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": {"message": exc.message, "type": exc.__class__.__name__}},
        )

    @app.exception_handler(UsernameAlreadyExistsException)
    @app.exception_handler(UserIdAlreadyExistsErrorException)
    async def user_id_already_exists_exception_handler(request, exc):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"error": {"message": exc.message, "type": exc.__class__.__name__}},
        )

    @app.exception_handler(UserIsDeletedException)
    async def user_is_deleted_exception_handler(request, exc):
        return JSONResponse(
            status_code=status.HTTP_410_GONE,
            content={"error": {"message": exc.message, "type": exc.__class__.__name__}},
        )


COMMON_RESPONSES = {
    status.HTTP_400_BAD_REQUEST: {
        "model": ErrorResponseSchema,
        "description": "Bad request data",
    },
    status.HTTP_404_NOT_FOUND: {
        "model": ErrorResponseSchema,
        "description": "Resource not found",
    },
    status.HTTP_409_CONFLICT: {
        "model": ErrorResponseSchema,
        "description": "Resource conflict",
    },
    status.HTTP_422_UNPROCESSABLE_ENTITY: {
        "model": ErrorResponseSchema,
        "description": "Validation error",
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "model": ErrorResponseSchema,
        "description": "Server error",
    },
}


# Create a helper function to add responses
def add_error_responses(
    response_dict: Dict[int, Dict[str, Any]], status_codes: list[int] = None
) -> Dict[int, Dict[str, Any]]:
    """Add common error responses to route responses dictionary"""
    result = response_dict.copy()

    # If specific status codes are provided, only add those
    if status_codes:
        for code in status_codes:
            if code in COMMON_RESPONSES:
                result[code] = COMMON_RESPONSES[code]
    # Otherwise add all common responses
    else:
        result.update(COMMON_RESPONSES)

    return result

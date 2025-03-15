from typing import TypeVar, Generic
from pydantic import BaseModel


class ErrorResponseSchema(BaseModel):
    error: dict = {"message": "Error message", "type": "ExceptionClassName"}


# IT = TypeVar("IT")
#
#
# class BaseQueryResponseSchema(BaseModel, Generic[IT]):
#     count: int
#     offset: int
#     limit: int
#     items: IT

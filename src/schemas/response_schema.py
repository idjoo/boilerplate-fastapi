from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class Response(BaseModel, Generic[T]):
    status: int = 200
    message: str = ""
    data: T | None

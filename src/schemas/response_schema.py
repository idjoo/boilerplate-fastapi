from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class Response(BaseModel, Generic[T]):  # noqa: UP046
    status: int = 200
    message: str = ""
    data: T | None

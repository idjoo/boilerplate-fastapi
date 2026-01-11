from pydantic import BaseModel


class Response[T](BaseModel):
    status: int = 200
    message: str = ""
    data: T | None

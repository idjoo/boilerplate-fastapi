from typing import Annotated

from fastapi import Depends
from httpx import AsyncClient


async def get_client() -> AsyncClient:
    async with AsyncClient(timeout=60) as client:
        yield client


HttpClient = Annotated[AsyncClient, Depends(get_client)]

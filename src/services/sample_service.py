from typing import Annotated
from uuid import UUID

from fastapi import Depends
from fastapi_pagination import Page

from src.dependencies import tracer

from src.models import (
    Sample,
    SampleCreate,
    SampleUpdate,
)
from src.repositories import SampleRepository


class SampleService:
    sample_repository: SampleRepository

    def __init__(
        self,
        sample_repository: Annotated[SampleRepository, Depends()],
    ) -> None:
        self.sample_repository = sample_repository

    @tracer.observe()
    async def create(
        self,
        sample: SampleCreate,
    ) -> Sample:
        return await self.sample_repository.create(sample)

    @tracer.observe()
    async def read_all(
        self,
    ) -> Page[Sample]:
        return await self.sample_repository.read_all()

    @tracer.observe()
    async def read(
        self,
        id: UUID,
    ) -> Sample | None:
        return await self.sample_repository.read(id=id)

    @tracer.observe()
    async def update(
        self,
        id: UUID,
        sample: SampleUpdate,
    ) -> Sample:
        return await self.sample_repository.update(id, sample)

    @tracer.observe()
    async def delete(
        self,
        id: UUID,
    ) -> None:
        return await self.sample_repository.delete(id=id)

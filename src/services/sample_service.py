from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi_pagination import Page
from sqlalchemy.exc import IntegrityError

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

    async def create(
        self,
        sample: SampleCreate,
    ) -> Sample:
        sample = await self.sample_repository.create(sample)

        return sample

    async def read_all(
        self,
    ) -> Page[Sample]:
        return await self.sample_repository.read_all()

    async def read(
        self,
        id: UUID,
    ) -> Sample | None:
        return await self.sample_repository.read(id=id)

    async def update(
        self,
        id: UUID,
        sample: SampleUpdate,
    ) -> Sample:
        return await self.sample_repository.update(id, sample)

    async def delete(
        self,
        id: UUID,
    ) -> None:
        return await self.sample_repository.delete(Sample(id=id))

from uuid import UUID

from fastapi_pagination import Page
from fastapi_pagination.ext.async_sqlmodel import paginate
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlmodel import delete, select, update

from src.dependencies import Database
from src.exceptions import SampleAlreadyExistsError, SampleNotFoundError
from src.models import (
    Sample,
    SampleCreate,
    SampleUpdate,
)


class SampleRepository:
    db: Database

    def __init__(self, db: Database) -> None:
        self.db = db

    async def create(
        self,
        sample: SampleCreate,
    ) -> Sample:
        try:
            data = Sample()
            data = data.model_validate(sample)
            self.db.add(data)
            await self.db.commit()
            await self.db.refresh(data)
        except IntegrityError:
            raise SampleAlreadyExistsError()

        return data

    async def read_all(
        self,
    ) -> Page[Sample]:
        return await paginate(
            self.db,
            select(Sample),
        )

    async def read(
        self,
        id: UUID,
    ) -> Sample | None:
        try:
            result = (
                await self.db.exec(
                    select(Sample).where(Sample.id == id),
                )
            ).one()
            await self.db.refresh(result)
        except NoResultFound:
            raise SampleAlreadyExistsError()

        return result

    async def update(
        self,
        id: UUID,
        sample: SampleUpdate,
    ) -> Sample:
        result = (
            await self.db.scalars(
                update(Sample)
                .where(Sample.id == id)
                .values(sample.model_dump(exclude_none=True))
                .returning(Sample),
            )
        ).one()
        await self.db.commit()
        await self.db.refresh(result)
        return result

    async def delete(
        self,
        sample: Sample,
    ) -> None:
        await self.db.exec(delete(Sample).where(Sample.id == sample.id))
        await self.db.commit()

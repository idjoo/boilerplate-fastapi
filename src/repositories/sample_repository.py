from uuid import UUID

from fastapi_pagination import Page
from fastapi_pagination.ext.async_sqlmodel import paginate
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlmodel import delete, select, update

from src.dependencies import Database
from src.exceptions import (
    SampleAlreadyExistsError,
    SampleError,
    SampleNotFoundError,
)
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
            return data
        except IntegrityError as error:
            raise SampleAlreadyExistsError() from error
        except Exception as error:
            raise SampleError("Database Internal Error") from error

    async def read_all(
        self,
    ) -> Page[Sample]:
        try:
            return await paginate(
                self.db,
                select(Sample),
            )
        except Exception as error:
            raise SampleError("Database Internal Error") from error

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
            return result
        except NoResultFound as error:
            raise SampleNotFoundError() from error
        except Exception as error:
            raise SampleError("Database Internal Error") from error

    async def update(
        self,
        id: UUID,
        sample: SampleUpdate,
    ) -> Sample:
        try:
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
        except Exception as error:
            raise SampleError("Database Internal Error") from error

    async def delete(
        self,
        id: UUID,
    ) -> None:
        try:
            await self.db.exec(delete(Sample).where(Sample.id == id))
            await self.db.commit()
        except Exception as error:
            raise SampleError("Database Internal Error") from error

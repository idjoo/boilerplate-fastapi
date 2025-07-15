from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class SampleBase(SQLModel):
    name: str = Field(default="default sample")


class Sample(SampleBase, table=True):
    __tablename__: str = "samples"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(
        default_factory=datetime.now,
        sa_column_kwargs={"onupdate": datetime.now},
    )


class SampleCreate(SampleBase):
    id: UUID


class SamplePublic(SampleBase):
    id: UUID


class SampleUpdate(SampleBase):
    name: str | None = None

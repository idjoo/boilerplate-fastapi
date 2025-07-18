from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi_pagination import Page

from src.dependencies import Logger, tracer
from src.models import (
    SampleCreate,
    SamplePublic,
    SampleUpdate,
)
from src.schemas import Response
from src.services import SampleService

router = APIRouter(
    prefix="/samples",
    tags=["sample"],
)


@router.post("/")
@tracer.observe
async def create(
    logger: Logger,
    sample_service: Annotated[SampleService, Depends()],
    sample: SampleCreate,
) -> Response[SamplePublic]:
    data = await sample_service.create(sample)
    return Response(
        status=status.HTTP_200_OK,
        message="Sample created successfully",
        data=data,
    )


@router.get("/")
@tracer.observe
async def read_all(
    logger: Logger,
    sample_service: Annotated[SampleService, Depends()],
) -> Page[SamplePublic]:
    data = await sample_service.read_all()
    return data


@router.get("/{id}")
@tracer.observe
async def read(
    logger: Logger,
    sample_service: Annotated[SampleService, Depends()],
    id: UUID,
) -> Response[SamplePublic]:
    data = await sample_service.read(id)
    return Response(
        status=status.HTTP_200_OK,
        message="Success",
        data=data,
    )


@router.patch("/{id}")
@tracer.observe
async def update(
    logger: Logger,
    sample_service: Annotated[SampleService, Depends()],
    id: UUID,
    sample: SampleUpdate,
) -> Response[SamplePublic]:
    data = await sample_service.update(id, sample)
    return Response(
        status=status.HTTP_200_OK,
        message="Successfully updated",
        data=data,
    )


@router.delete("/{id}")
@tracer.observe
async def delete(
    logger: Logger,
    sample_service: Annotated[SampleService, Depends()],
    id: UUID,
) -> Response:
    await sample_service.delete(id)
    return Response(
        status=status.HTTP_200_OK,
        message="Successfully deleted",
        data=None,
    )

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
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
    try:
        data = await sample_service.create(sample)
    except Exception as error:
        logger.error(error, exc_info=True)
        if not hasattr(error, "status_code"):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=Response(
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    message=str(error),
                    data=None,
                ).model_dump(),
            )
        raise HTTPException(
            status_code=error.status_code,
            detail=Response(
                status=error.status_code,
                message=f"{error.code}: {error.message}",
                data=None,
            ).model_dump(),
        )

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
    return await sample_service.read_all()


@router.get("/{id}")
@tracer.observe
async def read(
    logger: Logger,
    sample_service: Annotated[SampleService, Depends()],
    id: UUID,
) -> Response[SamplePublic]:
    try:
        data = await sample_service.read(id)
    except Exception as error:
        logger.error(error, exc_info=True)
        if not hasattr(error, "status_code"):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=Response(
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    message=str(error),
                    data=None,
                ).model_dump(),
            )
        raise HTTPException(
            status_code=error.status_code,
            detail=Response(
                status=error.status_code,
                message=f"{error.code}: {error.message}",
                data=None,
            ).model_dump(),
        )

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
    try:
        data = await sample_service.update(id, sample)
    except Exception as error:
        logger.error(error, exc_info=True)
        if not hasattr(error, "status_code"):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=Response(
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    message=str(error),
                    data=None,
                ).model_dump(),
            )
        raise HTTPException(
            status_code=error.status_code,
            detail=Response(
                status=error.status_code,
                message=f"{error.code}: {error.message}",
                data=None,
            ).model_dump(),
        )

    return Response(
        status=status.HTTP_200_OK,
        message="Successfully updated",
        data=data,
    )


@router.delete(
    "/{id}",
    status_code=status.HTTP_200_OK,
)
@tracer.observe
async def delete(
    logger: Logger,
    sample_service: Annotated[SampleService, Depends()],
    id: UUID,
) -> Response:
    try:
        await sample_service.delete(id)
    except Exception as error:
        logger.error(error, exc_info=True)
        if not hasattr(error, "status_code"):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=Response(
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    message=str(error),
                    data=None,
                ).model_dump(),
            )
        raise HTTPException(
            status_code=error.status_code,
            detail=Response(
                status=error.status_code,
                message=f"{error.code}: {error.message}",
                data=None,
            ).model_dump(),
        )

    return Response(
        status=status.HTTP_200_OK,
        message="Successfully deleted",
        data=None,
    )

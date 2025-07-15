from typing import Annotated
from urllib.parse import quote

from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from src.dependencies.config import Config, get_config
from src.dependencies.logger import Logger, get_logger

config: Config = get_config()
logger: Logger = get_logger(config)


async def create_engine() -> AsyncEngine:
    url = ""

    if config.database.url:
        url = config.database.url
    else:
        url = (
            f"{config.database.kind}+{config.database.adapter}://"
            f"{config.database.username}:{quote(config.database.password)}@"
            f"{config.database.host}:{config.database.port}/"
            f"{config.database.name}"
        )

    logger.info(f"creating database engine: {url}")

    return create_async_engine(url=url, echo=True, future=True)


async def init():
    engine = await create_engine()
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session(
    engine: Annotated[AsyncEngine, Depends(create_engine)],
) -> AsyncSession:
    logger.info("creating database session")

    session = sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )

    async with session() as session:
        yield session
        await session.close()

    logger.info("closing database session")


Database = Annotated[AsyncSession, Depends(get_session)]

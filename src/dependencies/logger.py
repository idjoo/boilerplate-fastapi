import logging
import sys
from typing import Annotated

from fastapi import Depends
from google.cloud.logging.handlers import StructuredLogHandler

from src.dependencies.config import Config, get_config

config: Config = get_config()


async def init():
    logger = logging.getLogger(config.service)
    logger.setLevel(config.logging.level.upper())
    logger.addHandler(StructuredLogHandler(stream=sys.stdout))


async def aget_logger() -> logging.Logger:
    return logging.getLogger(config.service)


def get_logger() -> logging.Logger:
    return logging.getLogger(config.service)


Logger = Annotated[logging.Logger, Depends(aget_logger)]

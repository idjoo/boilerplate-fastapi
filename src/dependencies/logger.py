import logging
import sys
from typing import Annotated

from fastapi import Depends
from google.cloud.logging.handlers import StructuredLogHandler
from opentelemetry import _logs
from opentelemetry.exporter.cloud_logging import (
    CloudLoggingExporter,
)
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource

from src.dependencies.config import Config, get_config

config: Config = get_config()


async def init():
    logger_provider = LoggerProvider(
        resource=Resource.create({"service.name": config.service}),
    )

    _logs.set_logger_provider(logger_provider)

    _logs.get_logger_provider().add_log_record_processor(
        BatchLogRecordProcessor(
            CloudLoggingExporter(default_log_name=config.service),
        )
    )

    logger = logging.getLogger(config.service)
    logger.setLevel(config.logging.level.upper())
    logger.addHandler(StructuredLogHandler(stream=sys.stdout))
    logger.addHandler(LoggingHandler())


async def aget_logger() -> logging.Logger:
    return logging.getLogger(config.service)


def get_logger() -> logging.Logger:
    return logging.getLogger(config.service)


Logger = Annotated[logging.Logger, Depends(aget_logger)]

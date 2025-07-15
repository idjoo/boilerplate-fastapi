import inspect
from collections.abc import Callable, Iterator
from contextlib import asynccontextmanager, contextmanager
from functools import wraps

from opentelemetry import trace
from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
from opentelemetry.propagate import set_global_textmap
from opentelemetry.propagators.cloud_trace_propagator import (
    CloudTraceFormatPropagator,
)
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.semconv.trace import SpanAttributes
from opentelemetry.trace import SpanKind
from opentelemetry.trace.span import Span
from opentelemetry.trace.status import StatusCode

from src.dependencies.config import Config, get_config

config: Config = get_config()


async def init():
    tracer_provider = TracerProvider(
        resource=Resource.create({"service.name": config.service}),
    )
    trace.set_tracer_provider(tracer_provider)

    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(CloudTraceSpanExporter())
    )

    set_global_textmap(CloudTraceFormatPropagator())


@asynccontextmanager
async def track(name: str) -> Iterator[Span]:
    tracer = trace.get_tracer(config.service)
    with tracer.start_as_current_span(
        name,
        kind=SpanKind.INTERNAL,
        record_exception=True,
        set_status_on_exception=True,
        end_on_exit=True,
    ) as span:
        span.set_attribute("service.name", config.service)
        yield span
        span.set_status(StatusCode.OK)


@contextmanager
def create_span(func: Callable):
    tracer = trace.get_tracer(config.service)
    with tracer.start_as_current_span(
        func.__qualname__,
        kind=SpanKind.INTERNAL,
        record_exception=True,
        set_status_on_exception=True,
        end_on_exit=True,
    ) as span:
        span.set_attribute("service.name", config.service)
        span.set_attribute(SpanAttributes.CODE_FUNCTION, func.__qualname__)
        span.set_attribute(SpanAttributes.CODE_NAMESPACE, func.__module__)
        span.set_attribute(SpanAttributes.CODE_FILEPATH, inspect.getfile(func))
        yield span
        span.set_status(StatusCode.OK)


def observe(func):
    @wraps(func)
    def _wrapper(*args, **kwargs):
        with create_span(func):
            return func(*args, **kwargs)

    @wraps(func)
    async def _awrapper(*args, **kwargs):
        with create_span(func):
            return await func(*args, **kwargs)

    if inspect.iscoroutinefunction(func):
        return _awrapper
    else:
        return _wrapper


__all__ = ["observe", "track"]

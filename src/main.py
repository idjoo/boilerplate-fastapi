from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi_pagination import add_pagination

from src.dependencies import Environment
from src.dependencies.config import Config, get_config
from src.dependencies.logger import Logger, get_logger
from src.exceptions import BaseError
from src.routers import HealthRouter, SampleRouter


@asynccontextmanager
async def lifespan(app: FastAPI):
    from src.dependencies import database, logger, tracer

    await database.init()
    await logger.init()
    await tracer.init()
    yield


config: Config = get_config()
logger: Logger = get_logger()


title = "Service Name - Swagger UI"  # TODO: service name


app = FastAPI(
    lifespan=lifespan,
    title=title,
    contact={
        "name": "Author - Devoteam",  # TODO: author name
        "url": "https://example.com",  # TODO: domain name
        "email": "author@example.com",  # TODO: author email
    },
    docs_url=None,
)


# ===============
# Middlewares
# ===============
add_pagination(app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ===============
# Routers
# ===============
app.include_router(HealthRouter)
app.include_router(SampleRouter)


# ===============
# Handlers
# ===============
@app.exception_handler(BaseError)
async def http_exception_handler(request, exception):
    logger.error(exception.message, exc_info=True)
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "status_code": exception.status_code,
            "message": exception.message,
            "data": None,
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exception):
    data = {}
    for error in exception.errors():
        loc, msg = error["loc"], error["msg"]
        filtered_loc = loc[1:] if loc[0] in ("body", "query", "path") else loc
        field_string = ".".join(filtered_loc)
        if field_string not in data:
            data[field_string] = []
        data[field_string].append(msg)

    return JSONResponse(
        status_code=400,
        content={
            "status_code": 400,
            "message": "Validation Error",
            "data": data,
        },
    )


# ===============
# Base Routers
# ===============
if config.environment != Environment.PRD:
    """Enable docs only for Development environment"""

    @app.get("/docs", include_in_schema=False)
    async def swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url="/openapi.json",
            title=title,
            swagger_ui_parameters=app.swagger_ui_parameters,
        )

    @app.get("/", include_in_schema=False)
    async def home():
        return RedirectResponse("/docs")


# ===============
# WSGI
# ===============
def server():
    uvicorn.run(
        app="src:app",
        host="0.0.0.0",
        port=config.port,
        log_level=config.logging.level.lower(),
        reload=True if config.environment == Environment.LOCAL else False,
    )

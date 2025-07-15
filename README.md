# FastAPI Boilerplate

A scalable, production-ready FastAPI backend boilerplate using modern Python best practices and a clean architecture approach.

## Features

- **FastAPI** for high-performance async APIs
- **SQLModel** for ORM and data modeling
- **Pydantic** for settings and validation
- **Google Cloud Logging** and **OpenTelemetry** for observability
- **Async database support** (PostgreSQL by default)
- **Pagination** and standard API response schemas
- **Docker** and **docker-compose** for containerization
- **Cloud Build** config for CI/CD
- Modular, extensible, and testable codebase

## Folder Structure

```
├── src/
│   ├── dependencies/   # Dependency injection: config, db, logger, tracer
│   ├── exceptions/     # Custom exception classes
│   ├── models/         # SQLModel ORM models
│   ├── repositories/   # Data access layer (repositories)
│   ├── routers/        # FastAPI routers (endpoints)
│   ├── schemas/        # Pydantic schemas for API and responses
│   ├── services/       # Business logic layer (services)
│   ├── __init__.py
│   ├── main.py         # Entrypoint (FastAPI app)
│   └── ...
├── config.yaml         # App configuration (can use .json/.toml too)
├── pyproject.toml      # Project metadata and dependencies
├── Dockerfile          # Docker build file
├── docker-compose.yml  # Local dev database
├── cloudbuild.yaml     # GCP Cloud Build config
└── README.md           # This file
```

## Design Patterns & Architecture

- **Dependency Injection**: All core resources (config, db, logger, tracer) are injected using FastAPI's Depends system.
- **Repository Pattern**: Data access is abstracted in `repositories/` for testability and separation of concerns.
- **Service Layer**: Business logic is encapsulated in `services/`.
- **Router Layer**: API endpoints are organized in `routers/`.
- **Schema Layer**: All request/response validation is handled by Pydantic models in `schemas/`.
- **Configurable**: Settings are loaded from YAML, JSON, TOML, or environment variables using Pydantic Settings.
- **Observability**: Integrated logging and tracing for production readiness.

## Getting Started

### 1. Clone the repository

```sh
git clone <your-repo-url>
cd <repo-name>
```

### 2. Configure your environment

Edit `config.yaml` (or use `config.json`/`config.toml`/`.env`) to set service name, database, and other settings.

### 3. Install dependencies

You can use [uv](https://github.com/astral-sh/uv) (recommended) or pip:

#### Using uv

```sh
uv sync
```

#### Using pip

```sh
pip install -r requirements.txt  # or use pyproject.toml with pip >= 23.1
```

### 4. Run the application

#### Locally

```sh
uv run app
```

### 5. API Docs

- Swagger UI: [http://localhost:8080/docs](http://localhost:8080/docs) (enabled in development)

## Extending the Boilerplate

- Add new models in `src/models/` and schemas in `src/schemas/`
- Implement new repositories in `src/repositories/`
- Add business logic in `src/services/`
- Register new routers in `src/routers/` and include them in `main.py`

## Configuration

- All settings can be managed via `config.yaml`, `config.json`, `config.toml`, or environment variables.
- See `src/dependencies/config.py` for all available options.

## Observability

- Logging is set up for Google Cloud Logging (can be customized)
- Distributed tracing via OpenTelemetry (GCP exporter by default)

## Testing & Linting

- Add your tests in a `tests/` directory (not included by default)
- Recommended tools: `pytest`, `pytest-asyncio`, `coverage`, `ruff`, `pre-commit`

## License

MIT (or specify your license)

---

> **Template by Vian** — Feel free to use, modify, and contribute!

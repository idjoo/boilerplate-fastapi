# Development Workflow

## Dependency Management

This project uses `uv` for fast and reliable dependency management.

- **Add a dependency**: `uv add <package>`
- **Add a dev dependency**: `uv add --dev <package>`
- **Sync environment**: `uv sync`

## Linting & Formatting

We use **Ruff** for both linting and formatting.

- **Check code**: `uv run ruff check .`
- **Fix issues**: `uv run ruff check --fix .`
- **Format code**: `uv run ruff format .`

## Testing

Tests are powered by **pytest**.

- **Run all tests**: `uv run pytest`
- **Run with coverage**: `uv run pytest --cov=src`

## Pre-commit Hooks

Ensure code quality before committing.

1.  Install hooks:
    ```sh
    uv run pre-commit install
    ```
2.  Run manually:
    ```sh
    uv run pre-commit run --all-files
    ```

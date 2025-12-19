# Database & Migrations

## ORM: SQLModel

We use **SQLModel** (which combines Pydantic and SQLAlchemy) for database interactions.

- **Models**: Defined in `src/models/`.
- **Async Support**: All database operations use `async`/`await`.

## Migrations: Alembic

Database schema changes are managed by **Alembic**.

### Common Commands

**Create a new migration** (after changing models):

```sh
uv run alembic revision --autogenerate -m "description_of_changes"
```

**Apply migrations**:

```sh
uv run alembic upgrade head
```

**Revert last migration**:

```sh
uv run alembic downgrade -1
```

## Repositories

Always access the database through Repositories. Do not use the raw session in Routers or Services if possible.

Example Repository Method:

```python
async def get_user(self, user_id: int) -> User | None:
    statement = select(User).where(User.id == user_id)
    result = await self.session.exec(statement)
    return result.first()
```

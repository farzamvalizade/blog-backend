# Backend API

This directory contains only the FastAPI JSON API and application logic. It does not serve frontend assets, render HTML, or use Jinja2. A separate client can consume the OpenAPI-described endpoints.

## Stack

- FastAPI and Uvicorn
- SQLModel with PostgreSQL
- Alembic migrations
- uv dependency management
- JWT superuser authentication

Feature modules live in `app/`. Each feature may contain its own models, schemas, repository, service, and router. `app/core/` contains shared configuration, database, security, and validation code.

## Local development

Start PostgreSQL from the repository root:

```bash
docker compose up -d db
```

Then run from this directory:

```bash
uv sync
uv run alembic upgrade head
uv run uvicorn app.main:app --reload
```

The API is available at <http://localhost:8000>, documentation at <http://localhost:8000/docs>, and health status at <http://localhost:8000/health>.

## Quality checks

```bash
uv run ruff check app
uv run ty check app
```

## Migrations

After changing a table model, import it through `app/models.py`, then run:

```bash
uv run alembic revision --autogenerate -m "describe the schema change"
uv run alembic upgrade head
```

Always review generated migrations before applying them.

# Repository Guidelines

## Project Purpose

This full-stack website is a portfolio, blog, and skills showcase for two Python developers. It publishes posts, presents skills, links deployed applications and source repositories, and highlights completed projects. Although it begins as our personal site, features should support general developer portfolio and publishing workflows.

## Architecture & Project Structure

Keep frontend and backend strictly separated. `backend/` contains only the FastAPI API, database access, migrations, and application logic. Do not add templates, frontend assets, Jinja2, or server-rendered pages there. React belongs in root-level `frontend/` and communicates through JSON APIs.

Use simple feature modules under `backend/app/`, such as `users/`, `auth/`, `posts/`, and `skills/`. Each feature owns its models, schemas, repository, service, and router when needed. Avoid unnecessary abstractions. Shared database, security, configuration, and validation code belongs in `backend/app/core/`. PostgreSQL is the application database; manage its schema with Alembic.

## Build, Test, and Development Commands

Run PostgreSQL and the API from the repository root:

```bash
docker compose up --build
```

For local Python development, run commands from `backend/`:

```bash
uv sync
uv run alembic upgrade head
uv run uvicorn app.main:app --reload
uv run pytest
uv run ruff check app tests
uv run ty check app
```

Keep all Node tooling inside `frontend/`; never add it to `backend/`.

## Coding Style & Naming Conventions

Use four-space indentation and modern Python annotations. Ruff enforces style and imports. Use `snake_case` for modules and functions, `PascalCase` for classes and schemas, and plural collection routes. Keep HTTP concerns in routers, rules in services, and SQLModel queries in repositories. React components use `PascalCase`; hooks begin with `use`.

## Testing Guidelines

Use Pytest for backend tests. Name files `test_*.py` and functions `test_<behavior>`. Mirror features under `backend/tests/` and cover authorization, validation, and persistence. Frontend tests stay in `frontend/`.

## Commit & Pull Request Guidelines

Use Conventional Commits with a lowercase type and an imperative description:

* `feat: add project showcase page`
* `fix: prevent duplicate post slugs`
* `refactor: use PyJWT for token handling`

Keep commits focused. Pull requests must summarize changes, identify migrations or configuration updates, list verification commands, and link issues. Include API examples for endpoints and screenshots for visible React changes.

## Security & Configuration

Never commit production secrets. Treat `.env` as local configuration, use strong deployment credentials, and never expose PostgreSQL publicly. Validate migrations and authorization dependencies before merging protected-route changes.

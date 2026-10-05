# Blog Backend

FastAPI, SQLModel, Alembic, and PostgreSQL foundation for a blog. Public clients can read published content and website information. A configured superuser can log in and manage posts, categories, tags, and site settings.

## Run everything with one command

### Requirements

Install Docker Engine or Docker Desktop with Docker Compose v2. Verify it with:

```bash
docker --version
docker compose version
```

### Start the stack

From the repository root, run:

```bash
docker compose up --build
```

This one command:

1. Builds the FastAPI image.
2. Starts PostgreSQL and waits until it is healthy.
3. Runs all Alembic migrations.
4. Creates the initial superuser if it does not already exist.
5. Starts the API on <http://localhost:8000>.

Useful URLs:

* API documentation: <http://localhost:8000/docs>
* OpenAPI document: <http://localhost:8000/api/v1/openapi.json>
* Health check: <http://localhost:8000/health>

Press `Ctrl+C` to stop the foreground stack. To run it in the background instead:

```bash
docker compose up --build -d
```

Check its status and follow backend logs with:

```bash
docker compose ps
docker compose logs -f backend
```

Stop the background stack while retaining database data:

```bash
docker compose down
```

## Configuration

Docker Compose automatically reads the repository's `.env` file. These variables are supported:

| Variable | Development default | Purpose |
| --- | --- | --- |
| `POSTGRES_DB` | `blog` | PostgreSQL database name |
| `POSTGRES_USER` | `blog` | PostgreSQL user |
| `POSTGRES_PASSWORD` | `blog_dev_password` | PostgreSQL password |
| `BACKEND_PORT` | `8000` | Host port for the API |
| `PROJECT_NAME` | `Blog API` | Name displayed in API documentation |
| `FASTAPI_ENV` | `development` | Application environment |
| `SECRET_KEY` | development-only value | JWT signing secret |
| `FIRST_SUPERUSER` | `admin@example.com` | Initial administrator email |
| `FIRST_SUPERUSER_PASSWORD` | `AdminPass123!` | Initial administrator password |
| `BACKEND_CORS_ORIGINS` | `[]` | JSON array of permitted frontend origins |

For example:

```dotenv
POSTGRES_DB=blog
POSTGRES_USER=blog
POSTGRES_PASSWORD=local_blog_password
BACKEND_PORT=8000

PROJECT_NAME=My Blog API
FASTAPI_ENV=development
SECRET_KEY=replace-with-a-long-random-secret
FIRST_SUPERUSER=admin@example.com
FIRST_SUPERUSER_PASSWORD=replace-with-a-strong-password
BACKEND_CORS_ORIGINS=["http://localhost:3000"]
```

Use a URL-safe PostgreSQL password because Compose inserts it into `DATABASE_URL`. Letters, numbers, `_`, and `-` are safe choices.

After changing application configuration, recreate the backend container:

```bash
docker compose up --build -d --force-recreate backend
```

The first-superuser settings only create a user when that email does not exist. Changing the password variable later does not replace the password stored in PostgreSQL.

## Administrator login

In Swagger UI, call `POST /api/v1/auth/login` as form data. The `username` field is the value of `FIRST_SUPERUSER`, and `password` is `FIRST_SUPERUSER_PASSWORD`.

With curl:

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=admin@example.com&password=AdminPass123!'
```

Copy the returned `access_token` and send it as a bearer token for protected create, update, and delete routes:

```bash
curl http://localhost:8000/api/v1/auth/me \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN'
```

There is no public registration endpoint and regular accounts cannot log in during this development stage.

## Database operations

Open PostgreSQL's command line:

```bash
docker compose exec db psql -U blog -d blog
```

Apply migrations manually if needed:

```bash
docker compose exec backend alembic upgrade head
```

Create a migration after changing SQLModel tables:

```bash
docker compose exec backend alembic revision --autogenerate -m "describe the change"
docker compose exec backend alembic upgrade head
```

PostgreSQL data is stored in the named `postgres_data` Docker volume. `docker compose down` retains it.

To completely reset the local database, including the superuser and all blog data:

```bash
docker compose down --volumes
docker compose up --build
```

The reset is destructive and cannot be undone unless the volume has been backed up.

## Development without Docker

Start only PostgreSQL:

```bash
docker compose up -d db
```

Then run the API locally from `backend/` with an appropriate `DATABASE_URL` whose host is `localhost`:

```bash
uv sync
uv run alembic upgrade head
uv run uvicorn app.main:app --reload
```

## Production notes

Before exposing this stack publicly:

* Set `FASTAPI_ENV=production`.
* Replace `SECRET_KEY`, `FIRST_SUPERUSER_PASSWORD`, and `POSTGRES_PASSWORD` with strong secrets.
* Restrict `BACKEND_CORS_ORIGINS` to trusted frontend origins.
* Put the backend behind an HTTPS reverse proxy.
* Back up the PostgreSQL volume regularly.
* Do not expose the PostgreSQL service port publicly.

The included Compose configuration intentionally exposes only the FastAPI port; PostgreSQL is reachable only inside the Compose network.

More backend details are available in [backend/README.md](backend/README.md).

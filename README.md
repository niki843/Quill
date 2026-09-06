# Quill
A modern, responsive blogging platform for creating, managing, and sharing posts.

## Stack

- **API**: [FastAPI](https://fastapi.tiangolo.com/)
- **Database**: PostgreSQL 17, accessed via SQLAlchemy 2.0's async ORM (`asyncpg` driver)
- **Validation/serialization**: Pydantic v2
- **Runtime**: Docker Compose (`api` + `db` services)

## Project layout

```
app/
  api/routes/   FastAPI routers (posts, comments)
  models/       SQLAlchemy ORM models
  schemas/      Pydantic request/response schemas
  db/           Engine, session factory, declarative base
  core/         Settings (env-driven config)
tests/          pytest suite (unit + integration)
```

## Running the app

```
make build   # docker compose build
make up      # start api + db
make logs    # follow logs
make down    # stop
```

Copy `.env.example` to `.env` and adjust as needed before the first run.

## Running tests

Tests use **pytest** + **pytest-asyncio**, with **httpx**'s `AsyncClient` driving the FastAPI app in-process (no server needed) against an **in-memory SQLite** database (via `aiosqlite`) instead of Postgres, so the suite runs fast and needs no Docker services up.

One-time setup:

```
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements-dev.txt   # Windows
# .venv/bin/pip install -r requirements-dev.txt                   # macOS/Linux
```

Then run:

```
make test
```

which runs `pytest` against the suite in `tests/`:
- `tests/test_schemas.py` — unit tests for the Pydantic schemas
- `tests/test_posts_api.py`, `tests/test_comments_api.py` — integration tests for the HTTP routes, seeded via fixtures in `tests/conftest.py`

# __PROJECT_NAME__

A Python/FastAPI microservice generated from AI Engineering Standard `__STANDARD_VERSION__` and the `__PROFILE_NAME__` profile `__PROFILE_VERSION__`.

## Architecture

See [architecture overview](docs/architecture/overview.md) and [ADRs](docs/architecture/decisions/). The initial orders endpoint uses in-memory data to validate the service shape. PostgreSQL is supplied by Compose for the future persistence adapter.

## Requirements

- Python 3.9 or newer
- Docker Desktop for Docker Compose

## Local Development

```sh
python3 -m venv .venv
. .venv/bin/activate
pip install ".[dev]"
uvicorn app.main:app --reload
```

Copy `.env.example` to `.env` when adding database-backed behavior.

## Docker Compose

```sh
docker compose up --build
```

The API is available at `http://localhost:8000`. OpenAPI documentation is at `/docs`.

## Tests

```sh
pytest
```

The suite includes unit, integration, and API workflow examples.

## API

- `GET /health`
- `GET /ready`
- `GET /api/v1/orders`
- `POST /api/v1/orders`
- `GET /api/v1/orders/{id}`
# AREA 303 — Backend (FastAPI)

FastAPI service for AREA 303. See repo root `README.md` for the full picture.

## Layout

```
backend/
├── app/
│   ├── api/                 # HTTP layer
│   │   ├── v1/
│   │   │   ├── endpoints/   # one router per feature
│   │   │   └── router.py    # aggregates v1 routers
│   │   └── deps.py          # shared FastAPI dependencies (db, redis, auth)
│   ├── core/                # config, security, responses, exceptions
│   ├── db/                  # SQLAlchemy session, base, redis client
│   ├── models/              # SQLAlchemy ORM models
│   ├── schemas/             # Pydantic request/response schemas
│   ├── services/            # business logic
│   ├── main.py              # FastAPI app factory
│   └── config.py            # pydantic-settings settings
├── alembic/                 # DB migrations (initialized on first run)
├── tests/                   # pytest tests mirror app/
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
└── .env.example
```

## Run locally

```bash
cp .env.example .env
docker compose -f ../docker-compose.yml up -d postgres redis
python -m venv .venv && . .venv/Scripts/Activate.ps1
pip install -r requirements-dev.txt
uvicorn app.main:app --reload --port 8000
```

## Tests

```bash
pytest
ruff check .
mypy app
```

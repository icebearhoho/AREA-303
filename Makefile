# Local dev helpers — pure documentation, not load-bearing.
# All commands assume your shell is at the repo root unless stated otherwise.

.PHONY: help install lint type test run up down migrate revision clean

help:
	@echo "Targets:"
	@echo "  install   create venv + pip install backend/dev requirements"
	@echo "  lint      ruff check backend"
	@echo "  type      mypy backend/app"
	@echo "  test      pytest (backend)"
	@echo "  run       uvicorn with reload (backend)"
	@echo "  up        docker compose up -d postgres redis backend"
	@echo "  down      docker compose down"
	@echo "  migrate   alembic upgrade head (backend)"
	@echo "  revision  alembic revision --autogenerate -m '...' (backend)"

install:
	python -m venv backend/.venv
	backend/.venv/Scripts/python -m pip install --upgrade pip
	backend/.venv/Scripts/python -m pip install -r backend/requirements-dev.txt

lint:
	cd backend && ruff check .

type:
	cd backend && mypy app

test:
	cd backend && pytest

run:
	cd backend && uvicorn app.main:app --reload --port 8000

up:
	docker compose up -d

down:
	docker compose down

migrate:
	cd backend && alembic upgrade head

revision:
	cd backend && alembic revision --autogenerate -m "$(name)"

clean:
	cd backend && rd /s /q .pytest_cache .mypy_cache .ruff_cache .coverage 2>nul || true

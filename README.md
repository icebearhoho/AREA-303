# AREA 303

Data + AI/ML **monorepo** for **ARRA 303 ("The Buffalo Playground")** — clothing & accessories + cosmetics/personal care on Vietnamese e-commerce platforms (Shopee, Tiki, Lazada).

This repo is organized as a small **monorepo**:

- `backend/` — FastAPI API service (Python 3.11)
- `frontend/` — Next.js 14 dashboard (App Router) — *to be added*
- `dataset/` — raw + processed datasets for the 17 candidate product ideas
- `docker-compose.yml` — local Postgres + Redis + backend
- `.github/workflows/` — CI pipelines

The `dataset/` folder already shipped; see `dataset/by_idea/idea_*` for the 17 ideas' cleaned datasets.

## Quick start (backend)

```bash
cp backend/.env.example backend/.env
docker compose up -d postgres redis
cd backend
python -m venv .venv
. .venv/Scripts/Activate.ps1   # PowerShell
pip install -r requirements.txt -r requirements-dev.txt
uvicorn app.main:app --reload --port 8000
```

OpenAPI docs: <http://localhost:8000/docs>

## API response standard

All JSON responses from the backend follow this envelope:

```json
{
  "success": true,
  "data": { "...": "..." },
  "meta": { "request_id": "...", "page": 1, "page_size": 20, "total": 0 },
  "error": null
}
```

On failure:

```json
{
  "success": false,
  "data": null,
  "meta": { "request_id": "..." },
  "error": { "code": "RESOURCE_NOT_FOUND", "message": "...", "details": {} }
}
```

See `backend/app/core/responses.py` for the implementation and `backend/app/core/exceptions.py` for the error codes.

## Contributing

Branch naming: `feat/<scope>-<short-desc>`, `fix/<scope>-<short-desc>`, `chore/<scope>`. Open PRs against `main`. CI must pass (lint + tests).

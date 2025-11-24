# FastAPI Tasks API

## Project layout
- `app/main.py` — FastAPI app and lifespan hook
- `app/core/` — settings and auth/backends (`config.py`, `auth.py`, `user_manager.py`)
- `app/db/` — SQLAlchemy base/session (`session.py`) and models (`models/`)
- `app/api/routes/` — HTTP routers (`auth.py`, `tasks.py`)
- `app/schemas/` — Pydantic schemas for tasks and users
- `app/repositories/` — DB-facing data access (`task.py`)
- `alembic/` — migrations (`versions/` holds migration files)

## Local run
1) Create venv and install deps  
`python -m venv venv && source venv/bin/activate && pip install -r requirements.txt`

2) Configure `.env` (fields map to `app/core/config.py`):
```
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/tasks
AUTH_SECRET=change_me
RESET_SECRET=change_me
VERIFY_SECRET=change_me
CORS_ORIGINS=["http://localhost:3000"]
COOKIE_SECURE=false
```

3) Run API  
`uvicorn app.main:app --reload`

4) Apply migrations  
`alembic upgrade head`

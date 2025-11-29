# Backend (FastAPI)

## Setup

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

## Environment

1. Скопируйте `env.example` в `.env` и при необходимости отредактируйте значения.
2. По умолчанию используется SQLite файл `app.db` в корне backend.

## Running

```bash
cd backend
uvicorn app.main:app --reload
```

API будет доступно по адресу http://localhost:8000, документация — http://localhost:8000/docs.

## Tests

```bash
cd backend
pytest
```


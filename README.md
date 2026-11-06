# ShopEase Auth Service

Python FastAPI authentication microservice with JWT access tokens, MySQL persistence, SQLAlchemy ORM, and Alembic migrations.

## Stack

- **Backend:** Python 3.11+, FastAPI, Uvicorn, Pydantic
- **Auth:** JWT (python-jose), Passlib / bcrypt
- **DB:** MySQL 8 + SQLAlchemy + Alembic
- **Runtime:** Docker Compose

## Features

- User register / login endpoints
- Password hashing and JWT issuance
- Layered routers / services / models / schemas
- Database migrations with Alembic

## Quick start

```bash
cp .env.example .env
docker compose up --build
```

API docs: http://localhost:8000/docs

## Author

Pooja Sharma — [Pooja101117](https://github.com/Pooja101117)

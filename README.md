# delivery_api

A RESTful API built to simulate a pizza delivery system. Covers user authentication with JWT, order management, and database migrations with Alembic.

## Tools

- FastAPI
- SQLAlchemy
- SQLite
- Alembic
- Pydantic
- python-jose
- passlib (bcrypt)
- python-dotenv

## Features

- User registration with encrypted password storage
- JWT authentication with access token (30 min) and refresh token (7 days)
- OAuth2 login compatible with Swagger UI
- Token validation via FastAPI dependency injection
- Order creation linked to authenticated users
- Database migrations managed with Alembic
- Modular structure separating routers, models, schemas and utilities

## Project Structure

```
delivery_api/
    app/
        models/
            base_model.py
            user.py
            order.py
        routers/
            __init__.py
            auth.py
            order.py
        schemas/
            base_schema.py
            user.py
            order.py
        utils/
            database.py
            dependencies.py
            load_env.py
            security.py
            request_test.py
    alembic/
    main.py
    alembic.ini
    requirements.txt
    .env
```

## Getting Started

Clone the repository and create a virtual environment:

```bash
git clone https://github.com/gabrielboniolo/delivery_api.git
cd delivery_api
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in the root directory:

```
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACESS_TOKEN_EXPIRE_MINUTES=30
```

Run migrations and start the server:

```bash
alembic upgrade head
uvicorn main:app --reload
```

API available at `http://127.0.0.1:8000` and interactive docs at `http://127.0.0.1:8000/docs`.

## Endpoints

**Auth**

| Method | Route | Description | Auth |
|--------|-------|-------------|------|
| GET | /auth/ | Status route | No |
| POST | /auth/criar_conta | Register new user | No |
| POST | /auth/login | Login, returns access + refresh token | No |
| POST | /auth/login-form | OAuth2 login for Swagger UI | No |
| GET | /auth/refresh | Get new access token via refresh token | Yes |

**Orders**

| Method | Route | Description | Auth |
|--------|-------|-------------|------|
| GET | /pedidos/ | Default route | No |
| POST | /pedidos/pedido | Create order | No |

## Authentication Flow

Login returns an access token (30 min) and a refresh token (7 days). Use the access token in the `Authorization: Bearer` header on protected routes. When it expires, call `/auth/refresh` with the refresh token to get a new one.

## Architecture Notes

`Base` is declared in `database.py` rather than `base_model.py` to avoid circular imports with Alembic's `env.py`. `BaseModel` uses `__abstract__ = True` so the `id` column is inherited by all models without generating its own table. `routers/__init__.py` centralizes router registration so `main.py` stays minimal. The `utils/` layer separates bcrypt and OAuth2 setup (`security.py`), environment loading (`load_env.py`), and session/token injection (`dependencies.py`).

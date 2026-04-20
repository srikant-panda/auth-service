# Auth Service

A FastAPI authentication microservice with JWT token management, email verification, refresh-token rotation, and OTP-based password recovery.

## Features

- User signup, signin, logout
- Email verification flow with tokenized link
- JWT access and refresh token handling
- Refresh token rotation and revocation
- Argon2 password hashing
- HTTP-only refresh token cookie
- OTP generation and email delivery for password recovery
- Reset password flow gated by verified OTP
- Async SQLAlchemy + PostgreSQL
- Docker support for PostgreSQL service

## Tech Stack

- FastAPI
- SQLAlchemy 2.0 (async)
- PostgreSQL 16
- python-jose (JWT)
- passlib (Argon2)
- aiosmtplib (SMTP)
- asyncpg

## Prerequisites

- Python 3.14+
- uv
- Docker + Docker Compose (optional, for DB)

## Installation

```bash
git clone https://github.com/srikant-panda/auth-service.git
cd auth-service
uv sync
```

## Environment Setup

### Local development

```bash
cp .env.example .env
```

### Docker DB configuration

```bash
cp .env.docker.example .env.docker
```

Set required variables in your environment file:

```env
BASE_URL="http://localhost:8000"
DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/auth_db"

SECRET_KEY="your-super-secret-key-change-this-in-production"
SECRET="your-super-secret-key-change-this-in-production"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

SMTP_HOST="smtp.gmail.com"
SMTP_PORT=465
SMTP_USER="your-email@gmail.com"
SMTP_PASSWORD="your-app-password"
```

## Run the Project

### 1) Start database with Docker

```bash
docker-compose up -d db
```

### 2) Start API locally

```bash
uv run uvicorn main:app --reload
```

API base URL: `http://localhost:8000`

## API Endpoints

Base prefix: `/api/user`

### Authentication

- `POST /signup`
- `POST /signin`
- `POST /refresh`
- `POST /logout`
- `GET /verify-email?token=<token>`

### Password Recovery (OTP)

- `POST /forget-password?email=<user_email>`
  - Generates OTP and sends it through email
- `PUT /verify-otp`
  - Marks OTP as verified
- `POST /reset-password`
  - Requires verified OTP record for the email

Example body for OTP verification:

```json
{
  "email": "john@example.com",
  "otp": "123456"
}
```

Example body for password reset:

```json
{
  "email": "john@example.com",
  "old_password": "current-password",
  "password": "new-password"
}
```

## Authentication Flow

1. User signs up.
2. Verification email is sent.
3. User verifies email via `GET /verify-email` token link.
4. User signs in and receives access token + refresh cookie.
5. Refresh endpoint rotates refresh token and returns new access token.
6. Logout removes current refresh token.

## Forgot Password Flow

1. Call `POST /forget-password` with user email.
2. Receive OTP in email.
3. Call `PUT /verify-otp` with email + OTP.
4. Call `POST /reset-password` with email, old password, and new password.

## Project Structure

```text
auth-service/
├── app/
│   ├── USER/
│   │   ├── UserPydanticModel.py
│   │   ├── UserRoute.py
│   │   └── UserService.py
│   ├── config/
│   ├── dependency/
│   ├── models/
│   └── services/
├── docker-compose.yml
├── Dockerfile
├── main.py
├── pyproject.toml
└── README.md
```

## API Docs

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## License

MIT

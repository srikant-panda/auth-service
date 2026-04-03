# Auth Service

A FastAPI-based authentication microservice with JWT token management, user registration, and secure password hashing using Argon2.

## Features

- User signup and signin
- JWT-based authentication with access and refresh tokens
- Argon2 password hashing
- HTTP-only cookie storage for refresh tokens
- Token refresh mechanism
- PostgreSQL database with async support
- Docker Compose setup for database and pgAdmin

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL 16
- **ORM**: SQLAlchemy 2.0 (async)
- **Authentication**: JWT (python-jose)
- **Password Hashing**: Argon2 (via passlib)
- **Database Driver**: asyncpg
- **Package Manager**: uv
- **Container**: Docker & Docker Compose

## Prerequisites

- Python 3.14 or higher
- uv package manager
- Docker & Docker Compose (for containerized database)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/srikant-panda/auth-service.git
cd auth-service
```

2. Install dependencies:
```bash
uv sync
```

3. Configure environment variables:
```bash
cp .env.example .env
```

Edit `.env` with your configuration:
```
DATABASE_URL="postgresql+asyncpg://admin:admin@localhost:5432/auth_db"
SECRET_KEY="your-secret-key-here"
```

## Database Setup

Start PostgreSQL and pgAdmin using Docker Compose:

```bash
docker-compose up -d
```

This will start:
- PostgreSQL on port 5432
- pgAdmin on port 5050 (admin@admin.com / admin)

## Running the Application

Start the FastAPI server:

```bash
uv run uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### User Authentication

**POST** `/api/user/signup`
- Register a new user
- Request body: `UserSignUPINfo`

**Request:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Response (201 Created):**
```json
{
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "John Doe",
    "email": "john@example.com",
    "role": "user"
  }
}
```

**Error Response (409 Conflict):**
```json
{
  "detail": "User with this email already exist. Please try another email."
}
```

---

**POST** `/api/user/signin`
- Authenticate user and receive tokens
- Request body: `UserSignININfo`
- Returns: Access token in response body, refresh token in HTTP-only cookie

**Request:**
```json
{
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Response (202 Accepted):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "msg": "User signed in."
}
```

**Error Responses:**

404 Not Found:
```json
{
  "detail": "User not found. Check the email."
}
```

401 Unauthorized:
```json
{
  "detail": "Invalid credentials"
}
```

---

**POST** `/api/user/refresh`
- Refresh access token using refresh token
- Requires: `refresh_token` cookie (automatically sent by browser)
- Returns: New access token and refresh token

**Response (202 Accepted):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "msg": "Token refreshed."
}
```

**Error Responses:**

401 Unauthorized:
```json
{
  "detail": "No refresh token given"
}
```

```json
{
  "detail": "Invalid refresh token"
}
```

```json
{
  "detail": "Token Expired."
}
```

## Project Structure

```
auth-service/
├── app/
│   ├── USER/
│   │   ├── UserPydanticModel.py   # Request/response schemas
│   │   ├── UserRoute.py           # API routes
│   │   └── UserService.py         # Business logic
│   ├── config/
│   │   └── db.py                  # Database configuration
│   ├── dependency/
│   │   └── dependecies.py         # FastAPI dependencies
│   ├── models/
│   │   └── user_model.py          # SQLAlchemy models
│   └── services/
│       ├── hash_service.py        # Password hashing (Argon2)
│       └── jwt_service.py         # JWT token management
├── .env                           # Environment variables
├── docker-compose.yml             # Database services
├── main.py                        # Application entry point
├── pyproject.toml                 # Project dependencies
└── README.md
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+asyncpg://admin:admin@localhost:5432/auth_db` |
| `SECRET_KEY` | JWT secret key | - |
| `ALGORITHM` | JWT signing algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token lifetime | `15` |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Refresh token lifetime | `7` |

## Authentication Flow

1. **Signup**: User registers with email/username and password
2. **Signin**: User authenticates and receives:
   - Access token (short-lived, 15 minutes)
   - Refresh token (long-lived, 7 days, stored as HTTP-only cookie)
3. **Access Protected Routes**: Include access token in Authorization header
4. **Token Refresh**: Use refresh endpoint to get new tokens before access token expires

## Security Features

- Argon2 password hashing (memory-hard, resistant to GPU attacks)
- JWT tokens with expiration
- HTTP-only cookies for refresh tokens (XSS protection)
- Separate access and refresh token lifecycle
- Token validation and error handling
- 
### Interactive API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## License

MIT

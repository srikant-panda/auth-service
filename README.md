# Auth Service

A production-ready FastAPI authentication microservice with JWT token management, email verification, role-based access control, and secure password hashing using Argon2.

## Features

- **User Authentication**: Signup, signin, and logout
- **Email Verification**: Automatic verification email on signup
- **JWT Token Management**: Access and refresh tokens with secure rotation
- **Password Security**: Argon2 password hashing (memory-hard, GPU-resistant)
- **HTTP-Only Cookies**: Refresh tokens stored securely (XSS protection)
- **Role-Based Access Control**: User roles for authorization
- **Token Refresh**: Automatic token rotation on refresh
- **Database Auditing**: Created/updated timestamps
- **Async Architecture**: Full async/await support with PostgreSQL
- **Docker Support**: Containerized database and pgAdmin

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL 16
- **ORM**: SQLAlchemy 2.0 (async)
- **Authentication**: JWT (python-jose)
- **Password Hashing**: Argon2 (via passlib)
- **Email**: aiosmtplib (async SMTP)
- **Database Driver**: asyncpg, psycopg2-binary
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
- Sends verification email automatically
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
  },
  "email_sent": true
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
- Returns: New access token and refresh token (old token is revoked)

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

---

**POST** `/api/user/logout`
- Logout user and revoke refresh token
- Requires: `refresh_token` cookie

**Response (200 OK):**
```json
{
  "msg": "User logged out successfully."
}
```

---

**POST** `/api/user/verify-email`
- Verify user email with token from verification email
- Query parameter: `token`

**Request:**
```
POST /api/user/verify-email?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response (200 OK):**
```json
{
  "msg": "Email verified successfully."
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
│       ├── jwt_service.py         # JWT token management
│       └── email_service.py       # Email verification service
├── .env                           # Environment variables (not tracked)
├── .env.example                   # Environment variables template
├── .gitignore                     # Git ignore rules
├── docker-compose.yml             # Database services
├── main.py                        # Application entry point
├── pyproject.toml                 # Project dependencies
└── README.md
```

## Configuration

### Environment Variables Setup

1. Create a `.env` file in the project root:

2. Configure the following variables in your `.env` file:

```env
# Database Configuration
DATABASE_URL="postgresql+asyncpg://admin:admin@localhost:5432/auth_db"

# Password Hashing
SECRET_KEY="your-super-secret-key-change-this-in-production"

# JWT Configuration
SECRET="your-super-secret-key-change-this-in-production"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# Email Configuration (for verification emails)
SMTP_HOST="smtp.gmail.com"
SMTP_PORT=587
SMTP_USER="your-email@gmail.com"
SMTP_PASSWORD="your-app-password"
```

### Environment Variables Reference

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DATABASE_URL` | PostgreSQL async connection string | `postgresql+asyncpg://admin:admin@localhost:5432/auth_db` | Yes |
| `SECRET_KEY` | Secret key for password hashing | - | Yes |
| `SECRET` | Secret key for JWT signing | - | Yes |
| `ALGORITHM` | JWT signing algorithm | `HS256` | No |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token expiration time | `15` | No |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Refresh token expiration time | `7` | No |
| `SMTP_HOST` | SMTP server hostname | `smtp.gmail.com` | No |
| `SMTP_PORT` | SMTP server port | `587` | No |
| `SMTP_USER` | Email address for sending verification emails | - | No |
| `SMTP_PASSWORD` | App password for SMTP authentication | - | No |

### Production Recommendations

- Use a strong, randomly generated `SECRET_KEY` (at least 32 characters)
- Set appropriate token expiration times based on your security requirements
- Use environment-specific database credentials
- Never commit `.env` file to version control

## Authentication Flow

1. **Signup**: User registers with name, email, and password
2. **Email Verification**: System sends verification email to user
3. **Verify Email**: User clicks verification link or uses token to verify email
4. **Signin**: User authenticates and receives:
   - Access token (short-lived, 15 minutes)
   - Refresh token (long-lived, 7 days, stored as HTTP-only cookie)
5. **Access Protected Routes**: Include access token in Authorization header
6. **Token Refresh**: Use refresh endpoint to get new tokens before access token expires
7. **Logout**: Revoke refresh token and clear cookies

## Security Features

- **Argon2 Password Hashing**: Memory-hard algorithm resistant to GPU and ASIC attacks
- **JWT Tokens with Expiration**: Time-limited access and refresh tokens
- **HTTP-Only Cookies**: Refresh tokens protected from XSS attacks
- **Token Rotation**: Old refresh tokens revoked on each refresh
- **Email Verification**: Ensures user email authenticity
- **Separate Token Lifecycle**: Independent access and refresh token management
- **Environment-Based Secrets**: No hardcoded credentials
- **Input Validation**: Pydantic models with strict validation
- **Database Model Security**: User passwords never exposed in API responses

## API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs` - Interactive API testing
- **ReDoc**: `http://localhost:8000/redoc` - Clean API documentation

## License

MIT

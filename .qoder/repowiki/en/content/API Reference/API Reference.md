# API Reference

<cite>
**Referenced Files in This Document**
- [README.md](file://README.md)
- [main.py](file://main.py)
- [UserRoute.py](file://app/USER/UserRoute.py)
- [UserPydanticModel.py](file://app/USER/UserPydanticModel.py)
- [UserService.py](file://app/USER/UserService.py)
- [jwt_service.py](file://app/services/jwt_service.py)
- [hash_service.py](file://app/services/hash_service.py)
- [dependecies.py](file://app/dependency/dependecies.py)
- [user_model.py](file://app/models/user_model.py)
- [db.py](file://app/config/db.py)
- [pyproject.toml](file://pyproject.toml)
- [email_service.py](file://app/services/email_service.py)
</cite>

## Update Summary
**Changes Made**
- Added documentation for new logout endpoint (/api/user/logout)
- Added documentation for new email verification endpoint (/api/user/verify-email)
- Updated authentication flow documentation to include email verification process
- Enhanced error handling documentation for email verification scenarios
- Updated API endpoints section with comprehensive coverage of all authentication endpoints

## Table of Contents
1. [Introduction](#introduction)
2. [Project Structure](#project-structure)
3. [Core Components](#core-components)
4. [Architecture Overview](#architecture-overview)
5. [API Endpoints](#api-endpoints)
6. [Security Implementation](#security-implementation)
7. [Configuration Management](#configuration-management)
8. [Database Schema](#database-schema)
9. [Usage Examples](#usage-examples)
10. [Troubleshooting Guide](#troubleshooting-guide)
11. [Conclusion](#conclusion)

## Introduction
This document provides comprehensive API documentation for the Auth Service, a FastAPI-based authentication microservice. The service implements JWT-based authentication with secure password hashing using Argon2, user registration and signin functionality, email verification system, and robust token management with refresh capabilities. The documentation covers all public API endpoints, request/response schemas, error handling, security features, and deployment configurations.

## Project Structure
The authentication service follows a modular FastAPI architecture with clear separation of concerns:

```mermaid
graph TB
subgraph "Application Layer"
MAIN["main.py<br/>FastAPI Application"]
ROUTER["UserRoute.py<br/>API Endpoints"]
SERVICE["UserService.py<br/>Business Logic"]
MODEL["UserPydanticModel.py<br/>Request/Response Schemas"]
END
subgraph "Service Layer"
JWT["jwt_service.py<br/>JWT Token Management"]
HASH["hash_service.py<br/>Password Hashing"]
EMAIL["email_service.py<br/>Email Verification"]
DEP["dependecies.py<br/>Dependency Injection"]
END
subgraph "Data Layer"
DBCFG["db.py<br/>Database Configuration"]
UMODEL["user_model.py<br/>SQLAlchemy Models"]
END
MAIN --> ROUTER
ROUTER --> SERVICE
SERVICE --> JWT
SERVICE --> HASH
SERVICE --> EMAIL
SERVICE --> DEP
SERVICE --> UMODEL
ROUTER --> MODEL
DBCFG --> UMODEL
```

**Diagram sources**
- [main.py:1-40](file://main.py#L1-L40)
- [UserRoute.py:1-33](file://app/USER/UserRoute.py#L1-L33)
- [UserService.py:1-205](file://app/USER/UserService.py#L1-L205)
- [jwt_service.py:1-43](file://app/services/jwt_service.py#L1-L43)
- [hash_service.py:1-20](file://app/services/hash_service.py#L1-L20)
- [email_service.py:1-20](file://app/services/email_service.py#L1-L20)
- [dependecies.py:1-31](file://app/dependency/dependecies.py#L1-L31)
- [user_model.py:1-37](file://app/models/user_model.py#L1-L37)
- [db.py:1-27](file://app/config/db.py#L1-L27)

**Section sources**
- [main.py:1-40](file://main.py#L1-L40)
- [UserRoute.py:1-33](file://app/USER/UserRoute.py#L1-L33)
- [UserService.py:1-205](file://app/USER/UserService.py#L1-L205)
- [UserPydanticModel.py:1-48](file://app/USER/UserPydanticModel.py#L1-L48)

## Core Components
The authentication service consists of several core components working together to provide secure user authentication and email verification:

- **FastAPI Application**: Main application entry point with lifespan management and router registration
- **User Router**: Handles all user-related API endpoints with proper status codes
- **User Service**: Implements business logic for user operations, token management, email verification, and validation
- **JWT Service**: Manages JWT token creation, validation, and decoding with configurable expiration including verification tokens
- **Hash Service**: Provides secure password hashing using Argon2 algorithm
- **Email Service**: Handles email verification emails with SMTP integration
- **Database Models**: SQLAlchemy ORM models for user management, token storage, and email verification
- **Dependency Injection**: Centralized dependency management and JWT validation utilities

**Section sources**
- [main.py:26-40](file://main.py#L26-L40)
- [UserRoute.py:8-33](file://app/USER/UserRoute.py#L8-L33)
- [UserService.py:13-205](file://app/USER/UserService.py#L13-L205)
- [jwt_service.py:8-43](file://app/services/jwt_service.py#L8-L43)
- [hash_service.py:6-20](file://app/services/hash_service.py#L6-L20)
- [email_service.py:4-20](file://app/services/email_service.py#L4-L20)

## Architecture Overview
The authentication service follows a layered architecture pattern with clear separation between presentation, business logic, and data access layers:

```mermaid
sequenceDiagram
participant Client as "Client Application"
participant API as "FastAPI Router"
participant Service as "User Service"
participant DB as "Database"
participant JWT as "JWT Service"
participant Hash as "Hash Service"
participant Email as "Email Service"
Client->>API : POST /api/user/signup
API->>Service : addUser(payload, db)
Service->>DB : Check user existence
DB-->>Service : User lookup result
Service->>Hash : hash_password(password)
Hash-->>Service : Hashed password
Service->>DB : Create new user
DB-->>Service : User created
Service->>Email : send_verification_email(email, user_id)
Email-->>Service : Email sent status
Service-->>API : User object + email_sent flag
API-->>Client : 201 Created
Client->>API : POST /api/user/signin
API->>Service : verifyUser(payload, response, db)
Service->>DB : Verify user credentials
DB-->>Service : User data
Service->>Hash : verify_password(password, hash)
Hash-->>Service : Verification result
Service->>JWT : createAccessToken(user_id)
JWT-->>Service : Access token
Service->>JWT : createRefreshToken(user_id)
JWT-->>Service : Refresh token
Service->>DB : Store hashed refresh token
DB-->>Service : Token stored
Service-->>API : Access token + Set cookie
API-->>Client : 202 Accepted + HTTP-only cookie
Client->>API : POST /api/user/verify-email?token=JWT_TOKEN
API->>Service : verifyEmail(token, db)
Service->>JWT : decode(token)
JWT-->>Service : Decoded token data
Service->>DB : Update user.is_varified = True
DB-->>Service : User updated
Service-->>API : Success message
API-->>Client : 200 OK
Client->>API : POST /api/user/logout
API->>Service : signout(refresh_token, db, response)
Service->>JWT : decode(refresh_token)
JWT-->>Service : User ID from token
Service->>DB : Delete refresh token row
DB-->>Service : Token revoked
Service-->>API : Success message + cookie deleted
API-->>Client : 200 OK
```

**Diagram sources**
- [UserRoute.py:10-29](file://app/USER/UserRoute.py#L10-L29)
- [UserService.py:13-205](file://app/USER/UserService.py#L13-L205)
- [jwt_service.py:17-43](file://app/services/jwt_service.py#L17-L43)
- [hash_service.py:10-18](file://app/services/hash_service.py#L10-L18)
- [email_service.py:6-20](file://app/services/email_service.py#L6-L20)

## API Endpoints

### User Authentication Endpoints

#### POST /api/user/signup
User registration endpoint for creating new accounts.

**Request Body**: `UserSignUPINfo`
```json
{
  "name": "string",
  "email": "string",
  "password": "string"
}
```

**Response**: `UserOutInfo`
```json
{
  "user": {
    "id": "string",
    "name": "string",
    "email": "string",
    "role": "string"
  },
  "email_sent": true
}
```

**Status Codes**:
- `201 Created`: User successfully registered
- `409 Conflict`: User with email already exists

**Error Response**:
```json
{
  "detail": "User with this email already exist. Please try another email."
}
```

**Section sources**
- [UserRoute.py:10-12](file://app/USER/UserRoute.py#L10-L12)
- [UserService.py:13-31](file://app/USER/UserService.py#L13-L31)
- [UserPydanticModel.py:23-31](file://app/USER/UserPydanticModel.py#L23-L31)

#### POST /api/user/signin
User authentication endpoint for login and token issuance.

**Request Body**: `UserSignININfo`
```json
{
  "email": "string",
  "password": "string"
}
```

**Response**: `JwtOut`
```json
{
  "access_token": "string",
  "msg": "string"
}
```

**Cookies**:
- `refresh_token`: HTTP-only cookie containing refresh token

**Status Codes**:
- `202 Accepted`: User authenticated successfully
- `404 Not Found`: User not found
- `401 Unauthorized`: Invalid credentials
- `403 Forbidden`: Email not verified (when user exists but hasn't verified email)

**Success Response**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "msg": "User signed in."
}
```

**Error Responses**:
```json
{
  "detail": "User not found. Check the email."
}
```

```json
{
  "detail": "Invalid credentials"
}
```

```json
{
  "detail": "Email not verified. Check your email."
}
```

**Section sources**
- [UserRoute.py:13-15](file://app/USER/UserRoute.py#L13-L15)
- [UserService.py:33-82](file://app/USER/UserService.py#L33-L82)
- [UserPydanticModel.py:32-39](file://app/USER/UserPydanticModel.py#L32-L39)

#### POST /api/user/refresh
Token refresh endpoint for obtaining new access tokens using refresh tokens.

**Request**: Cookie-based authentication
- `refresh_token`: HTTP-only cookie (automatically sent by browser)

**Response**: `JwtOut`
```json
{
  "access_token": "string",
  "msg": "string"
}
```

**Status Codes**:
- `202 Accepted`: Token refreshed successfully
- `401 Unauthorized`: No refresh token provided, invalid refresh token, or expired token

**Success Response**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "msg": "Token refreshed."
}
```

**Error Responses**:
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

**Section sources**
- [UserRoute.py:17-21](file://app/USER/UserRoute.py#L17-L21)
- [UserService.py:85-124](file://app/USER/UserService.py#L85-L124)
- [UserPydanticModel.py:37-48](file://app/USER/UserPydanticModel.py#L37-L48)

#### POST /api/user/logout
User logout endpoint for terminating sessions and revoking refresh tokens.

**Request**: Cookie-based authentication
- `refresh_token`: HTTP-only cookie (automatically sent by browser)

**Response**: `Base`
```json
{
  "msg": "string"
}
```

**Cookies**:
- `refresh_token`: HTTP-only cookie (deleted upon successful logout)

**Status Codes**:
- `200 OK`: User logged out successfully
- `401 Unauthorized`: No refresh token provided or invalid refresh token

**Success Response**:
```json
{
  "msg": "User Loged Out"
}
```

**Error Responses**:
```json
{
  "detail": "No refresh token given"
}
```

**Section sources**
- [UserRoute.py:22-25](file://app/USER/UserRoute.py#L22-L25)
- [UserService.py:126-144](file://app/USER/UserService.py#L126-L144)
- [UserPydanticModel.py:10-13](file://app/USER/UserPydanticModel.py#L10-L13)

#### POST /api/user/verify-email
Email verification endpoint for confirming user email addresses.

**Query Parameters**:
- `token`: JWT verification token sent to user's email

**Response**: `Base`
```json
{
  "msg": "string"
}
```

**Status Codes**:
- `200 OK`: Email verified successfully
- `400 Bad Request`: Invalid token or token expired
- `404 Not Found`: User not found

**Success Response**:
```json
{
  "msg": "Email verify successfully."
}
```

**Error Responses**:
```json
{
  "detail": "Invalid token or expired"
}
```

```json
{
  "detail": "Invalid token"
}
```

```json
{
  "detail": "User not found"
}
```

**Section sources**
- [UserRoute.py:27-29](file://app/USER/UserRoute.py#L27-L29)
- [UserService.py:145-169](file://app/USER/UserService.py#L145-L169)
- [UserPydanticModel.py:10-13](file://app/USER/UserPydanticModel.py#L10-L13)

## Security Implementation

### Password Hashing
The service uses Argon2 password hashing algorithm for secure password storage:

- **Algorithm**: Argon2 (memory-hard, resistant to GPU attacks)
- **Implementation**: via passlib CryptContext
- **Security**: Automatic salting and configurable cost parameters

### JWT Token Management
Comprehensive token-based authentication system:

- **Access Tokens**: Short-lived (15 minutes) for API access
- **Refresh Tokens**: Long-lived (7 days) for token renewal
- **Verification Tokens**: Very short-lived (5 minutes) for email verification
- **Token Types**: Separate access, refresh, and verification token lifecycle management
- **Storage**: Refresh tokens stored as HTTP-only cookies (XSS protection)
- **Validation**: Comprehensive token validation and error handling

### Email Verification System
Secure email verification process:

- **Token Generation**: 5-minute expiry verification tokens
- **Email Delivery**: SMTP-based email sending with Gmail configuration
- **User Status**: Email verification flag prevents login until verified
- **Security**: Token-based verification prevents unauthorized access

### Database Security
- **Connection String**: Configurable via environment variables
- **Schema Isolation**: Uses dedicated "auth" schema
- **Token Storage**: Hashed refresh tokens stored in database
- **Session Management**: Async database sessions with proper cleanup

**Section sources**
- [hash_service.py:6-20](file://app/services/hash_service.py#L6-L20)
- [jwt_service.py:8-43](file://app/services/jwt_service.py#L8-L43)
- [email_service.py:4-20](file://app/services/email_service.py#L4-L20)
- [user_model.py:26-37](file://app/models/user_model.py#L26-L37)

## Configuration Management

### Environment Variables
The service requires the following environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+asyncpg://admin:admin@localhost:5432/auth_db` |
| `SECRET_KEY` | JWT secret key for token signing | - |
| `ALGORITHM` | JWT signing algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token lifetime in minutes | `15` |
| `REFRESH_TOKEN_EXPIIRE_DAYS` | Refresh token lifetime in days | `7` |

### Application Configuration
- **Python Version**: 3.14 or higher
- **Database**: PostgreSQL 16 with asyncpg driver
- **ORM**: SQLAlchemy 2.0 with async support
- **Framework**: FastAPI with automatic API documentation
- **Package Manager**: uv

**Section sources**
- [db.py:10-11](file://app/config/db.py#L10-L11)
- [jwt_service.py:9-13](file://app/services/jwt_service.py#L9-L13)
- [pyproject.toml:6-16](file://pyproject.toml#L6-L16)

## Database Schema

### User Model
The user table stores user account information:

```mermaid
erDiagram
USERS {
uuid id PK
string name
string email UK
string password
string role
boolean is_varified
timestamp createdAt
timestamp updatedAt
}
TOKEN {
integer id PK
string refresh_token
uuid user_id FK
uuid jti
boolean revoked
timestamp createdAt
timestamp expire_at
}
USERS ||--o{ TOKEN : has
```

**Diagram sources**
- [user_model.py:11-24](file://app/models/user_model.py#L11-L24)
- [user_model.py:26-37](file://app/models/user_model.py#L26-L37)

### Key Features
- **User Accounts**: Unique email addresses, role-based access control, email verification status
- **Token Management**: Hashed refresh tokens with expiration tracking and revocation
- **Audit Trail**: Creation and modification timestamps
- **Foreign Key Relationships**: Secure association between users and tokens

**Section sources**
- [user_model.py:1-37](file://app/models/user_model.py#L1-L37)

## Usage Examples

### Complete Authentication Flow with Email Verification
```mermaid
sequenceDiagram
participant Client as "Client"
participant Signup as "POST /api/user/signup"
participant Email as "Verification Email"
participant Verify as "POST /api/user/verify-email"
participant Signin as "POST /api/user/signin"
participant Refresh as "POST /api/user/refresh"
participant Logout as "POST /api/user/logout"
Client->>Signup : Register new user
Signup-->>Client : 201 Created with user data + email_sent flag
Client->>Email : Receive verification email
Email-->>Client : Email with verification link
Client->>Verify : Click verification link
Verify-->>Client : 200 OK + Email verified
Client->>Signin : Authenticate user
Signin-->>Client : 202 Accepted + Access token + Refresh cookie
Client->>Refresh : Refresh access token
Refresh-->>Client : 202 Accepted + New access token + New refresh cookie
Client->>Logout : Logout user
Logout-->>Client : 200 OK + Cookie deleted
```

### Error Handling Examples
The service provides comprehensive error responses:

**Registration Error**:
```json
{
  "detail": "User with this email already exist. Please try another email."
}
```

**Authentication Errors**:
```json
{
  "detail": "User not found. Check the email."
}
```

```json
{
  "detail": "Invalid credentials"
}
```

```json
{
  "detail": "Email not verified. Check your email."
}
```

**Token Refresh Errors**:
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

**Email Verification Errors**:
```json
{
  "detail": "Invalid token or expired"
}
```

```json
{
  "detail": "Invalid token"
}
```

```json
{
  "detail": "User not found"
}
```

**Logout Errors**:
```json
{
  "detail": "No refresh token given"
}
```

**Section sources**
- [UserService.py:17](file://app/USER/UserService.py#L17)
- [UserService.py:36-44](file://app/USER/UserService.py#L36-L44)
- [UserService.py:87-100](file://app/USER/UserService.py#L87-L100)
- [UserService.py:150-157](file://app/USER/UserService.py#L150-L157)
- [UserService.py:128](file://app/USER/UserService.py#L128)

## Troubleshooting Guide

### Common Issues and Solutions

**Database Connection Problems**
- Verify `DATABASE_URL` environment variable is correctly configured
- Ensure PostgreSQL server is running and accessible
- Check network connectivity and firewall settings

**JWT Configuration Issues**
- Ensure `SECRET_KEY` environment variable is set
- Verify JWT algorithm matches server configuration
- Check token expiration settings if tokens expire too quickly

**Authentication Failures**
- Verify user credentials are correct
- Check if user account exists in database
- Ensure password hashing is working correctly
- Verify user email is marked as verified for login attempts

**Token Refresh Issues**
- Verify refresh token cookie is being sent with requests
- Check refresh token validity and expiration
- Ensure database connection for token validation

**Email Verification Issues**
- Verify verification email is being sent successfully
- Check SMTP configuration for email service
- Ensure verification token is not expired (5-minute limit)
- Verify user exists in database before verification

**Logout Issues**
- Verify refresh token cookie is present during logout
- Check that refresh token exists in database
- Ensure proper cookie deletion on successful logout

**Deployment Issues**
- Verify Python 3.14+ is installed
- Ensure all dependencies are properly installed
- Check Docker Compose configuration if using containers

**Section sources**
- [db.py:21-27](file://app/config/db.py#L21-L27)
- [jwt_service.py:14](file://app/services/jwt_service.py#L14)
- [UserService.py:16](file://app/USER/UserService.py#L16)
- [email_service.py:13-20](file://app/services/email_service.py#L13-L20)

## Conclusion
The Auth Service provides a comprehensive, secure, and production-ready authentication solution built with modern Python technologies. The service offers robust user management, secure token-based authentication, email verification system, and flexible configuration options. The detailed API documentation, comprehensive error handling, and security-focused design make it suitable for integration into larger applications requiring reliable authentication services.

The modular architecture ensures maintainability and extensibility, while the FastAPI framework provides excellent developer experience with automatic API documentation and validation. The service is designed for scalability and can be easily deployed in various environments including containerized deployments using Docker Compose.

The addition of email verification and logout functionality enhances the service's security posture and user experience, providing complete lifecycle management for user authentication flows.
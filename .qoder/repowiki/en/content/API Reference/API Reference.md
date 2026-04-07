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
</cite>

## Update Summary
**Changes Made**
- Complete rewrite of API documentation to reflect the authentication service structure
- Added comprehensive API reference for user authentication endpoints
- Documented FastAPI application architecture and routing
- Added detailed response examples and error handling specifications
- Included security features and token management documentation
- Updated project structure visualization and configuration details

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
This document provides comprehensive API documentation for the Auth Service, a FastAPI-based authentication microservice. The service implements JWT-based authentication with secure password hashing using Argon2, user registration and signin functionality, and robust token management with refresh capabilities. The documentation covers all public API endpoints, request/response schemas, error handling, security features, and deployment configurations.

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
SERVICE --> DEP
SERVICE --> UMODEL
ROUTER --> MODEL
DBCFG --> UMODEL
```

**Diagram sources**
- [main.py:1-31](file://main.py#L1-L31)
- [UserRoute.py:1-23](file://app/USER/UserRoute.py#L1-L23)
- [UserService.py:1-105](file://app/USER/UserService.py#L1-L105)
- [jwt_service.py:1-38](file://app/services/jwt_service.py#L1-L38)
- [hash_service.py:1-20](file://app/services/hash_service.py#L1-L20)
- [dependecies.py:1-31](file://app/dependency/dependecies.py#L1-L31)
- [user_model.py:1-34](file://app/models/user_model.py#L1-L34)
- [db.py:1-27](file://app/config/db.py#L1-L27)

**Section sources**
- [main.py:1-31](file://main.py#L1-L31)
- [UserRoute.py:1-23](file://app/USER/UserRoute.py#L1-L23)
- [UserService.py:1-105](file://app/USER/UserService.py#L1-L105)
- [UserPydanticModel.py:1-47](file://app/USER/UserPydanticModel.py#L1-L47)

## Core Components
The authentication service consists of several core components working together to provide secure user authentication:

- **FastAPI Application**: Main application entry point with lifespan management and router registration
- **User Router**: Handles all user-related API endpoints with proper status codes
- **User Service**: Implements business logic for user operations, token management, and validation
- **JWT Service**: Manages JWT token creation, validation, and decoding with configurable expiration
- **Hash Service**: Provides secure password hashing using Argon2 algorithm
- **Database Models**: SQLAlchemy ORM models for user management and token storage
- **Dependency Injection**: Centralized dependency management and JWT validation utilities

**Section sources**
- [main.py:25-31](file://main.py#L25-L31)
- [UserRoute.py:8-22](file://app/USER/UserRoute.py#L8-L22)
- [UserService.py:13-105](file://app/USER/UserService.py#L13-L105)
- [jwt_service.py:8-38](file://app/services/jwt_service.py#L8-L38)
- [hash_service.py:6-20](file://app/services/hash_service.py#L6-L20)

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
Client->>API : POST /api/user/signup
API->>Service : addUser(payload, db)
Service->>DB : Check user existence
DB-->>Service : User lookup result
Service->>Hash : hash_password(password)
Hash-->>Service : Hashed password
Service->>DB : Create new user
DB-->>Service : User created
Service-->>API : User object
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
```

**Diagram sources**
- [UserRoute.py:10-21](file://app/USER/UserRoute.py#L10-L21)
- [UserService.py:13-62](file://app/USER/UserService.py#L13-L62)
- [jwt_service.py:16-31](file://app/services/jwt_service.py#L16-L31)
- [hash_service.py:10-18](file://app/services/hash_service.py#L10-L18)

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
    "password": "string",
    "role": "string"
  }
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
- [UserService.py:13-23](file://app/USER/UserService.py#L13-L23)
- [UserPydanticModel.py:23-30](file://app/USER/UserPydanticModel.py#L23-L30)

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

**Section sources**
- [UserRoute.py:13-15](file://app/USER/UserRoute.py#L13-L15)
- [UserService.py:25-62](file://app/USER/UserService.py#L25-L62)
- [UserPydanticModel.py:31-38](file://app/USER/UserPydanticModel.py#L31-L38)

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
- [UserService.py:65-105](file://app/USER/UserService.py#L65-L105)
- [UserPydanticModel.py:36-47](file://app/USER/UserPydanticModel.py#L36-L47)

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
- **Token Types**: Separate access and refresh token lifecycle management
- **Storage**: Refresh tokens stored as HTTP-only cookies (XSS protection)
- **Validation**: Comprehensive token validation and error handling

### Database Security
- **Connection String**: Configurable via environment variables
- **Schema Isolation**: Uses dedicated "auth" schema
- **Token Storage**: Hashed refresh tokens stored in database
- **Session Management**: Async database sessions with proper cleanup

**Section sources**
- [hash_service.py:6-20](file://app/services/hash_service.py#L6-L20)
- [jwt_service.py:8-38](file://app/services/jwt_service.py#L8-L38)
- [user_model.py:23-34](file://app/models/user_model.py#L23-L34)

## Configuration Management

### Environment Variables
The service requires the following environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+asyncpg://admin:admin@localhost:5432/auth_db` |
| `SECRET_KEY` | JWT secret key for token signing | - |
| `ALGORITHM` | JWT signing algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token lifetime in minutes | `15` |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Refresh token lifetime in days | `7` |

### Application Configuration
- **Python Version**: 3.14 or higher
- **Database**: PostgreSQL 16 with asyncpg driver
- **ORM**: SQLAlchemy 2.0 with async support
- **Framework**: FastAPI with automatic API documentation
- **Package Manager**: uv

**Section sources**
- [db.py:10-11](file://app/config/db.py#L10-L11)
- [jwt_service.py:9-12](file://app/services/jwt_service.py#L9-L12)
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
- [user_model.py:8-21](file://app/models/user_model.py#L8-L21)
- [user_model.py:23-34](file://app/models/user_model.py#L23-L34)

### Key Features
- **User Accounts**: Unique email addresses, role-based access control
- **Token Management**: Hashed refresh tokens with expiration tracking
- **Audit Trail**: Creation and modification timestamps
- **Foreign Key Relationships**: Secure association between users and tokens

**Section sources**
- [user_model.py:1-34](file://app/models/user_model.py#L1-L34)

## Usage Examples

### Basic Authentication Flow
```mermaid
sequenceDiagram
participant Client as "Client"
participant Signup as "POST /api/user/signup"
participant Signin as "POST /api/user/signin"
participant Refresh as "POST /api/user/refresh"
Client->>Signup : Register new user
Signup-->>Client : 201 Created with user data
Client->>Signin : Authenticate user
Signin-->>Client : 202 Accepted + Access token + Refresh cookie
Client->>Refresh : Refresh access token
Refresh-->>Client : 202 Accepted + New access token + New refresh cookie
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

**Section sources**
- [UserService.py:17](file://app/USER/UserService.py#L17)
- [UserService.py:28-36](file://app/USER/UserService.py#L28-L36)
- [UserService.py:68-83](file://app/USER/UserService.py#L68-L83)

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

**Token Refresh Issues**
- Verify refresh token cookie is being sent with requests
- Check refresh token validity and expiration
- Ensure database connection for token validation

**Deployment Issues**
- Verify Python 3.14+ is installed
- Ensure all dependencies are properly installed
- Check Docker Compose configuration if using containers

**Section sources**
- [db.py:21-27](file://app/config/db.py#L21-L27)
- [jwt_service.py:13-14](file://app/services/jwt_service.py#L13-L14)
- [UserService.py:16](file://app/USER/UserService.py#L16)

## Conclusion
The Auth Service provides a comprehensive, secure, and production-ready authentication solution built with modern Python technologies. The service offers robust user management, secure token-based authentication, and flexible configuration options. The detailed API documentation, comprehensive error handling, and security-focused design make it suitable for integration into larger applications requiring reliable authentication services.

The modular architecture ensures maintainability and extensibility, while the FastAPI framework provides excellent developer experience with automatic API documentation and validation. The service is designed for scalability and can be easily deployed in various environments including containerized deployments using Docker Compose.
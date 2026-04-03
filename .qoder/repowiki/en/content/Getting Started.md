# Getting Started

<cite>
**Referenced Files in This Document**
- [pyproject.toml](file://pyproject.toml)
- [main.py](file://main.py)
- [README.md](file://README.md)
- [uv.lock](file://uv.lock)
- [app/config/db.py](file://app/config/db.py)
- [app/USER/UserRoute.py](file://app/USER/UserRoute.py)
- [app/USER/UserService.py](file://app/USER/UserService.py)
- [app/dependency/dependecies.py](file://app/dependency/dependecies.py)
- [app/services/hash_service.py](file://app/services/hash_service.py)
- [app/services/jwt_service.py](file://app/services/jwt_service.py)
- [app/models/user_model.py](file://app/models/user_model.py)
</cite>

## Table of Contents
1. [Introduction](#introduction)
2. [Project Structure](#project-structure)
3. [Core Components](#core-components)
4. [Architecture Overview](#architecture-overview)
5. [Detailed Component Analysis](#detailed-component-analysis)
6. [Dependency Analysis](#dependency-analysis)
7. [Performance Considerations](#performance-considerations)
8. [Troubleshooting Guide](#troubleshooting-guide)
9. [Conclusion](#conclusion)
10. [Appendices](#appendices)

## Introduction
Auth Service is a modern Python authentication and authorization system built with FastAPI. It provides comprehensive user management capabilities including user registration, login, JWT-based authentication, refresh token handling, and secure password hashing. The service follows best practices for security and scalability, utilizing asynchronous database operations and robust cryptographic implementations.

The project emphasizes clean architecture with clear separation of concerns across models, services, routes, and dependencies. It leverages SQLAlchemy for ORM operations, Argon2 for secure password hashing, and JWT for stateless authentication tokens.

## Project Structure
The project follows a modular FastAPI architecture with clear separation of concerns:

```
auth-service/
├── app/
│   ├── USER/                    # User management module
│   │   ├── UserPydanticModel.py  # Pydantic models for user operations
│   │   ├── UserRoute.py         # FastAPI routes for user endpoints
│   │   ├── UserService.py       # Business logic for user operations
│   │   └── __init__.py
│   ├── config/                  # Database and configuration management
│   │   ├── __init__.py
│   │   └── db.py               # Database connection and session management
│   ├── dependency/              # Application dependencies and utilities
│   │   ├── __init__.py
│   │   └── dependecies.py      # Dependency injection and validation
│   ├── models/                 # Database models
│   │   ├── __init__.py
│   │   └── user_model.py       # User and token database models
│   └── services/               # Business logic services
│       ├── __init__.py
│       ├── hash_service.py     # Password hashing utilities
│       └── jwt_service.py      # JWT token management
├── pyproject.toml             # Project configuration and dependencies
├── main.py                    # Application entry point
├── README.md                  # Project documentation
└── uv.lock                   # Dependency lock file
```

**Section sources**
- [main.py:1-31](file://main.py#L1-L31)
- [pyproject.toml:1-17](file://pyproject.toml#L1-L17)

## Core Components
The authentication service consists of several interconnected components working together to provide secure user management:

### Database Layer
- **Database Configuration**: Centralized database connection management with async support
- **Models**: SQLAlchemy declarative models for users and refresh tokens with proper schema management
- **Session Management**: Async session factory with proper lifecycle management

### Service Layer
- **Hash Service**: Password hashing using Argon2 with secure random salt generation
- **JWT Service**: Token creation, validation, and decoding with configurable algorithms and expiration
- **Business Logic**: User operations including registration, authentication, and token refresh

### Application Layer
- **Routes**: RESTful endpoints for user registration, login, and token refresh
- **Dependency Injection**: Centralized dependency management and validation
- **Pydantic Models**: Data validation and serialization for API requests and responses

**Section sources**
- [app/config/db.py:1-27](file://app/config/db.py#L1-L27)
- [app/models/user_model.py:1-34](file://app/models/user_model.py#L1-L34)
- [app/services/hash_service.py:1-20](file://app/services/hash_service.py#L1-L20)
- [app/services/jwt_service.py:1-38](file://app/services/jwt_service.py#L1-L38)
- [app/USER/UserRoute.py:1-23](file://app/USER/UserRoute.py#L1-L23)

## Architecture Overview
The system follows a layered architecture pattern with clear separation between presentation, business logic, and data access layers.

```mermaid
graph TB
A["FastAPI Application<br/>main.py"] --> B["User Routes<br/>UserRoute.py"]
B --> C["User Service<br/>UserService.py"]
C --> D["Business Logic<br/>HashService & JwtService"]
D --> E["Database Models<br/>user_model.py"]
E --> F["Database Session<br/>db.py"]
F --> G["SQLAlchemy Engine<br/>AsyncPG Driver"]
H["Environment Config<br/>.env files"] --> D
H --> F
```

**Diagram sources**
- [main.py:25-31](file://main.py#L25-L31)
- [app/USER/UserRoute.py:8-23](file://app/USER/UserRoute.py#L8-L23)
- [app/USER/UserService.py:13-62](file://app/USER/UserService.py#L13-L62)
- [app/services/hash_service.py:6-18](file://app/services/hash_service.py#L6-L18)
- [app/services/jwt_service.py:8-38](file://app/services/jwt_service.py#L8-L38)
- [app/config/db.py:17-27](file://app/config/db.py#L17-L27)

## Detailed Component Analysis

### Installation and Environment Setup
The project uses uv as the package manager and supports both pip and direct installation methods:

**Installation Methods:**
- Direct installation: `pip install auth-service`
- Development installation: `pip install -e .`
- Using uv: `uv pip install auth-service`

**Environment Configuration:**
- Database URL: `DATABASE_URL` for PostgreSQL connection
- Security: `SECRET_KEY` for JWT encryption
- Algorithm: `ALGORITHM` for JWT signing (default: HS256)
- Token Expiration: `ACCESS_TOKEN_EXPIRE_MINUTES` and `REFRESH_TOKEN_EXPIRE_DAYS`

**Section sources**
- [pyproject.toml:1-17](file://pyproject.toml#L1-L17)
- [app/services/jwt_service.py:8-14](file://app/services/jwt_service.py#L8-L14)
- [app/config/db.py:10-11](file://app/config/db.py#L10-L11)

### Database Schema and Models
The system manages two primary tables with proper schema isolation:

**User Model:**
- UUID primary key with automatic generation
- Unique email constraint for user identification
- Role-based access control with default "user" role
- Timestamp tracking for creation and modification

**Refresh Token Model:**
- Hashed token storage for security
- Foreign key relationship to user table
- Revocation tracking and expiration management
- JSON Web Token ID (JTI) for individual token tracking

**Section sources**
- [app/models/user_model.py:8-34](file://app/models/user_model.py#L8-L34)

### Authentication Flow
The authentication system implements a comprehensive JWT-based workflow:

```mermaid
sequenceDiagram
participant Client as "Client Application"
participant Auth as "Authentication Service"
participant DB as "Database"
participant Hash as "Hash Service"
participant JWT as "JWT Service"
Client->>Auth : POST /api/user/signup
Auth->>DB : Check user existence
DB-->>Auth : User not found
Auth->>Hash : Hash password
Hash-->>Auth : Hashed password
Auth->>DB : Create user record
DB-->>Auth : User created
Client->>Auth : POST /api/user/signin
Auth->>DB : Verify user credentials
DB-->>Auth : Valid user
Auth->>Hash : Verify password
Hash-->>Auth : Password verified
Auth->>JWT : Create access token
Auth->>JWT : Create refresh token
Auth->>DB : Store refresh token hash
DB-->>Auth : Token stored
Auth-->>Client : Access token + refresh token
Client->>Auth : POST /api/user/refresh
Auth->>DB : Validate refresh token
DB-->>Auth : Valid token
Auth->>JWT : Create new access token
Auth->>DB : Store new refresh token
DB-->>Auth : New token stored
Auth-->>Client : New access token
```

**Diagram sources**
- [app/USER/UserService.py:13-62](file://app/USER/UserService.py#L13-L62)
- [app/USER/UserService.py:65-105](file://app/USER/UserService.py#L65-L105)
- [app/services/hash_service.py:10-18](file://app/services/hash_service.py#L10-L18)
- [app/services/jwt_service.py:16-31](file://app/services/jwt_service.py#L16-L31)

### API Endpoints
The service provides three main endpoints for user management:

**POST /api/user/signup**
- Creates new user accounts with unique email validation
- Hashes passwords using Argon2 algorithm
- Returns user information excluding sensitive data

**POST /api/user/signin**
- Authenticates existing users with credential verification
- Generates both access and refresh JWT tokens
- Sets refresh token as HTTP-only cookie for security

**POST /api/user/refresh**
- Validates refresh tokens and generates new access tokens
- Handles token revocation and cleanup
- Updates refresh token storage with new hashed tokens

**Section sources**
- [app/USER/UserRoute.py:10-22](file://app/USER/UserRoute.py#L10-L22)

### Security Features
The system implements multiple layers of security:

**Password Security:**
- Argon2 hashing with automatic salt generation
- Secure password verification without plaintext exposure
- SHA-256 token hashing for refresh token storage

**Token Security:**
- JWT tokens with configurable expiration times
- Separate access and refresh token types
- HTTP-only cookies for refresh token protection
- JTI (JSON Web Token ID) for individual token tracking

**Database Security:**
- Asynchronous database operations for performance
- Proper session management and cleanup
- Schema isolation with dedicated auth schema

**Section sources**
- [app/services/hash_service.py:6-18](file://app/services/hash_service.py#L6-L18)
- [app/services/jwt_service.py:8-38](file://app/services/jwt_service.py#L8-L38)
- [app/models/user_model.py:23-34](file://app/models/user_model.py#L23-L34)

## Dependency Analysis
The project relies on a carefully selected set of dependencies optimized for performance and security:

**Core Dependencies:**
- **FastAPI**: Web framework with automatic OpenAPI documentation
- **SQLAlchemy**: Object-relational mapping with async support
- **AsyncPG**: High-performance PostgreSQL driver
- **Argon2-cffi**: Secure password hashing implementation
- **Python-Jose**: JWT token handling and validation
- **Passlib**: Cryptographic password hashing library

**Development Dependencies:**
- **Alembic**: Database migration management
- **Python-Dotenv**: Environment variable management
- **Uv**: Modern Python package manager

```mermaid
graph LR
A["FastAPI Core"] --> B["SQLAlchemy ORM"]
B --> C["AsyncPG Driver"]
D["Argon2-cffi"] --> E["Password Security"]
F["Python-Jose"] --> G["JWT Operations"]
H["Passlib"] --> D
I["Alembic"] --> B
J["Python-Dotenv"] --> K["Environment Config"]
```

**Diagram sources**
- [pyproject.toml:7-16](file://pyproject.toml#L7-L16)

**Section sources**
- [pyproject.toml:1-17](file://pyproject.toml#L1-L17)
- [uv.lock:1-17](file://uv.lock#L1-L17)

## Performance Considerations
The system is designed for optimal performance through several architectural choices:

**Asynchronous Operations:**
- Full async/await support throughout the application
- Non-blocking database operations using AsyncPG
- Efficient session management with proper lifecycle handling

**Connection Pooling:**
- SQLAlchemy's async session factory for connection reuse
- Proper database connection cleanup and disposal
- Schema-aware connection management

**Security Throughput:**
- Optimized Argon2 parameters for balanced security/performance
- Efficient JWT encoding/decoding operations
- Minimal database round trips through bulk operations

**Memory Management:**
- Proper resource cleanup in lifespan handlers
- Efficient Pydantic model serialization
- Minimal object copying during authentication flows

## Troubleshooting Guide
Common issues and their solutions:

**Database Connection Issues:**
- Verify DATABASE_URL format: `postgresql+asyncpg://user:password@host:port/database`
- Ensure PostgreSQL server is accessible and accepting connections
- Check database credentials and network connectivity

**JWT Configuration Errors:**
- Set SECRET_KEY environment variable for token signing
- Verify ALGORITHM matches client expectations (default: HS256)
- Check token expiration settings for appropriate values

**Password Hashing Failures:**
- Ensure Argon2-cffi is properly installed
- Verify SECRET_KEY environment variable is set
- Check Python version compatibility (requires Python 3.14+)

**Authentication Failures:**
- Verify user exists in database before login attempts
- Check password hashing consistency between registration and login
- Ensure refresh tokens are properly stored and not expired

**Section sources**
- [app/config/db.py:10-11](file://app/config/db.py#L10-L11)
- [app/services/jwt_service.py:13-14](file://app/services/jwt_service.py#L13-L14)
- [app/services/hash_service.py:7](file://app/services/hash_service.py#L7)

## Conclusion
Auth Service provides a robust, secure, and scalable foundation for authentication and authorization needs. Its modular architecture, comprehensive security features, and efficient implementation make it suitable for production deployments. The clear separation of concerns, proper error handling, and extensive documentation facilitate easy maintenance and extension.

The system successfully balances security requirements with performance considerations, making it an excellent choice for applications requiring reliable user management capabilities.

## Appendices

### A. Installation Commands
- **Direct Installation**: `pip install auth-service`
- **Development Mode**: `pip install -e .`
- **Using uv**: `uv pip install auth-service`

**Section sources**
- [pyproject.toml:1-17](file://pyproject.toml#L1-L17)

### B. Environment Variables Reference
- **DATABASE_URL**: PostgreSQL connection string
- **SECRET_KEY**: JWT signing secret
- **ALGORITHM**: JWT algorithm (default: HS256)
- **ACCESS_TOKEN_EXPIRE_MINUTES**: Access token lifetime
- **REFRESH_TOKEN_EXPIRE_DAYS**: Refresh token lifetime

**Section sources**
- [app/services/jwt_service.py:8-14](file://app/services/jwt_service.py#L8-L14)
- [app/config/db.py:10-11](file://app/config/db.py#L10-L11)

### C. API Endpoint Reference
- **POST /api/user/signup**: User registration with validation
- **POST /api/user/signin**: User authentication and token generation
- **POST /api/user/refresh**: Refresh token validation and renewal

**Section sources**
- [app/USER/UserRoute.py:10-22](file://app/USER/UserRoute.py#L10-L22)

### D. Database Schema Overview
- **Users Table**: Stores user credentials and profile information
- **Token Table**: Manages refresh tokens with revocation tracking
- **Schema Isolation**: Dedicated "auth" schema for separation of concerns

**Section sources**
- [app/models/user_model.py:8-34](file://app/models/user_model.py#L8-L34)
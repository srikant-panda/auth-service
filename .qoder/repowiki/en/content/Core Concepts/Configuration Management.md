# Configuration Management

<cite>
**Referenced Files in This Document**
- [db.py](file://app/config/db.py)
- [jwt_service.py](file://app/services/jwt_service.py)
- [hash_service.py](file://app/services/hash_service.py)
- [email_service.py](file://app/services/email_service.py)
- [main.py](file://main.py)
- [docker-compose.yml](file://docker-compose.yml)
- [Dockerfile](file://Dockerfile)
- [.gitignore](file://.gitignore)
- [.dockerignore](file://.dockerignore)
- [README.md](file://README.md)
</cite>

## Update Summary
**Changes Made**
- Enhanced configuration system documentation to reflect centralized BASE_URL environment variable management
- Updated database credential standardization from 'admin' to 'postgres' throughout configuration documentation
- Improved environment variable templates coverage for local and Docker deployment scenarios
- Expanded security configuration guidelines with production recommendations
- Added comprehensive troubleshooting guide for BASE_URL and environment variable issues
- Updated Docker deployment configuration with environment file management

## Table of Contents
1. [Introduction](#introduction)
2. [Project Structure](#project-structure)
3. [Core Components](#core-components)
4. [Architecture Overview](#architecture-overview)
5. [Detailed Component Analysis](#detailed-component-analysis)
6. [Environment Variable Management](#environment-variable-management)
7. [Environment Variable Templates](#environment-variable-templates)
8. [Docker Deployment Configuration](#docker-deployment-configuration)
9. [Version Control Configuration](#version-control-configuration)
10. [Security Configuration](#security-configuration)
11. [Configuration Best Practices](#configuration-best-practices)
12. [Troubleshooting Guide](#troubleshooting-guide)
13. [Conclusion](#conclusion)
14. [Appendices](#appendices)

## Introduction
This document explains the authentication service configuration management system with a focus on environment variable handling, security considerations, and deployment best practices. The system has been enhanced with comprehensive environment variable templates, centralized BASE_URL support for email verification links, and standardized database credentials using 'postgres' instead of 'admin'. The repository now includes proper environment variable management through dedicated template files and Docker-specific configurations.

Key aspects covered:
- Environment variable loading and precedence with BASE_URL support
- Comprehensive environment variable templates (.env.example, .env.docker.example)
- Standardized database credentials and Docker integration
- Security-conscious configuration separation
- Multi-environment deployment strategies
- Troubleshooting common configuration issues

## Project Structure
The configuration system centers around environment variable templates and standardized database credentials, with proper Docker integration and version control separation:

```mermaid
graph TB
A["Environment Templates"] --> B[".env.example<br/>(Local Development)"]
A --> C[".env.docker.example<br/>(Docker Deployment)"]
B --> D["BASE_URL<br/>DATABASE_URL<br/>SECRET_KEY<br/>SECRET"]
C --> E["BASE_URL<br/>DATABASE_URL<br/>SECRET_KEY<br/>SECRET"]
F["Docker Integration"] --> G["docker-compose.yml<br/>env_file: .env.docker"]
G --> H["PostgreSQL Container<br/>postgres/postgres"]
I["Application Configuration"] --> J["FastAPI App<br/>Environment Loading"]
J --> K["Database Engine<br/>SQLAlchemy Async"]
L["Version Control"] --> M[".gitignore<br/>.env<br/>.env.docker"]
```

**Diagram sources**
- [README.md:277-280](file://README.md#L277-L280)
- [docker-compose.yml:10-11](file://docker-compose.yml#L10-L11)
- [db.py:7-9](file://app/config/db.py#L7-L9)

**Section sources**
- [README.md:277-280](file://README.md#L277-L280)
- [docker-compose.yml:10-11](file://docker-compose.yml#L10-L11)
- [db.py:7-9](file://app/config/db.py#L7-L9)

## Core Components
The configuration system consists of five main components with comprehensive environment variable support and Docker integration:

### Environment Variable Templates
- **.env.example**: Template for local development environment variables
- **.env.docker.example**: Template for Docker deployment environment variables
- **Template Variables**: BASE_URL, DATABASE_URL, SECRET_KEY, SECRET, ALGORITHM, token expirations

### Database Configuration
- **BASE_URL**: Application base URL for email verification links and redirect URLs
- **DATABASE_URL**: PostgreSQL async connection string with standardized 'postgres' credentials
- **Default Schema**: "auth" schema for database organization
- **Connection Pooling**: SQLAlchemy async engine with statement cache disabled

### Security Services
- **HashService**: Password hashing using Argon2 with SECRET_KEY for cryptographic operations
- **JwtService**: JWT token management using SECRET for signing operations with configurable algorithms

### Docker Integration
- **Dockerfile**: Python 3.13 slim container with environment variable support
- **docker-compose.yml**: Multi-service setup with PostgreSQL database and application container
- **Environment Files**: Separate .env and .env.docker files for different deployment contexts

**Section sources**
- [README.md:277-280](file://README.md#L277-L280)
- [db.py:7-16](file://app/config/db.py#L7-L16)
- [hash_service.py:6-8](file://app/services/hash_service.py#L6-L8)
- [jwt_service.py:8-16](file://app/services/jwt_service.py#L8-L16)
- [Dockerfile:1-10](file://Dockerfile#L1-L10)
- [docker-compose.yml:1-23](file://docker-compose.yml#L1-L23)

## Architecture Overview
The configuration pipeline follows a template-driven approach with environment variable precedence and Docker-aware deployment strategies:

```mermaid
sequenceDiagram
participant Template as "Environment Templates"
participant Docker as "Docker Compose"
participant EnvFile as ".env/.env.docker"
participant Loader as "dotenv.load_dotenv()"
participant App as "Application"
Template->>Docker : .env.docker.example
Docker->>EnvFile : Copy to .env.docker
EnvFile->>Loader : Load environment variables
Loader->>App : BASE_URL, DATABASE_URL, SECRET_KEY, SECRET
App->>App : Initialize database engine
App->>App : Configure JWT services
App->>App : Setup FastAPI application
```

**Diagram sources**
- [README.md:57-64](file://README.md#L57-L64)
- [docker-compose.yml:10-11](file://docker-compose.yml#L10-L11)
- [db.py:7](file://app/config/db.py#L7)

## Detailed Component Analysis

### Environment Variable Loading
The system utilizes python-dotenv for secure environment variable loading from template files. Both HashService and JwtService use environment variables loaded from .env files, with proper validation and error handling. The new BASE_URL variable supports email verification links and application redirects.

### Database Configuration Enhancement
- **BASE_URL Integration**: New BASE_URL variable for application base URL configuration
- **Standardized Credentials**: Database credentials now use 'postgres'/'postgres' instead of 'admin'/'admin'
- **Docker Host Support**: DATABASE_URL uses 'db' service name for Docker deployments
- **Schema Management**: Default schema set to "auth" for organized database structure

### Security Service Configuration
- **HashService**: Uses SECRET_KEY for Argon2 password hashing operations with passlib CryptContext
- **JwtService**: Uses SECRET for JWT token signing with configurable ALGORITHM and token expiration
- **Runtime Validation**: Both services validate required environment variables during initialization

### Docker Deployment Integration
- **Multi-stage Configuration**: Separate environment templates for local and Docker deployments
- **Service Dependencies**: Application container depends on PostgreSQL service
- **Port Mapping**: Application runs on port 8000, database on port 5432
- **Environment File Loading**: Docker Compose loads .env.docker environment variables

**Section sources**
- [README.md:294-301](file://README.md#L294-L301)
- [db.py:7-16](file://app/config/db.py#L7-L16)
- [hash_service.py:6-8](file://app/services/hash_service.py#L6-L8)
- [jwt_service.py:8-16](file://app/services/jwt_service.py#L8-L16)
- [docker-compose.yml:10-11](file://docker-compose.yml#L10-L11)

## Environment Variable Management

### Comprehensive Environment Variables Reference
| Variable | Description | Default | Required | Environment Context |
|----------|-------------|---------|----------|-------------------|
| `BASE_URL` | Application base URL for email verification links | `http://localhost:8000` | Yes | All environments |
| `DATABASE_URL` | PostgreSQL async connection string | `postgresql+asyncpg://postgres:postgres@localhost:5432/auth_db` | Yes | All environments |
| `SECRET_KEY` | Secret key for password hashing (Argon2) | - | Yes | All environments |
| `SECRET` | Secret key for JWT signing | - | Yes | All environments |
| `ALGORITHM` | JWT signing algorithm | `HS256` | No | All environments |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token expiration (minutes) | `15` | No | All environments |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Refresh token expiration (days) | `7` | No | All environments |
| `SMTP_HOST` | SMTP server hostname | `smtp.gmail.com` | No | Email functionality |
| `SMTP_PORT` | SMTP server port | `587` | No | Email functionality |
| `SMTP_USER` | Email address for verification emails | - | No | Email functionality |
| `SMTP_PASSWORD` | App password for SMTP authentication | - | No | Email functionality |

### Environment Variable Templates
The system provides comprehensive template files for different deployment scenarios:

**Local Development Template (.env.example)**
- Uses localhost for database connection
- Development-friendly defaults
- Suitable for direct Python execution

**Docker Deployment Template (.env.docker.example)**
- Uses 'db' service name for database connection
- Docker-specific host configuration
- Designed for containerized deployment

### Variable Separation Benefits
The separation of configuration variables provides:
- **Security Isolation**: Different cryptographic operations use distinct keys
- **Deployment Flexibility**: Environment-specific configurations through templates
- **Standardization**: Consistent database credentials across environments
- **Compliance Support**: Meets security standards requiring key separation

**Section sources**
- [README.md:325-340](file://README.md#L325-L340)
- [README.md:294-301](file://README.md#L294-L301)

## Environment Variable Templates

### Template File Structure
The project includes comprehensive environment variable templates for different deployment scenarios:

```mermaid
graph LR
A["Template System"] --> B[".env.example<br/>Local Development"]
A --> C[".env.docker.example<br/>Docker Deployment"]
B --> D["BASE_URL=http://localhost:8000"]
B --> E["DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/auth_db"]
C --> F["BASE_URL=http://localhost:8000"]
C --> G["DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/auth_db"]
D --> H["Application Configuration"]
E --> H
F --> H
G --> H
```

**Diagram sources**
- [README.md:53-64](file://README.md#L53-L64)
- [README.md:299-300](file://README.md#L299-L300)

### Template Usage Workflow
1. **Copy Template**: Copy .env.example to .env for local development
2. **Edit Configuration**: Modify variables according to your environment
3. **Environment Loading**: Application automatically loads variables from .env
4. **Docker Deployment**: Copy .env.docker.example to .env.docker for containerized deployment

### Template Customization Guidelines
- **Local Development**: Use localhost for database connections
- **Docker Deployment**: Use 'db' service name for database connections
- **Production Security**: Replace default secrets with cryptographically secure values
- **URL Configuration**: Ensure BASE_URL matches your deployment domain and port

**Section sources**
- [README.md:53-64](file://README.md#L53-L64)
- [README.md:299-300](file://README.md#L299-L300)

## Docker Deployment Configuration

### Multi-Service Architecture
The Docker deployment uses a two-service architecture with proper environment variable management:

```mermaid
graph TB
A["Docker Compose"] --> B["Application Service (app)"]
A --> C["Database Service (db)"]
B --> D["Python 3.13 Slim"]
B --> E[".env.docker Environment File"]
C --> F["PostgreSQL 16"]
C --> G["postgres/postgres Credentials"]
E --> H["Environment Variables Loaded"]
H --> I["Application Configuration"]
I --> J["Database Connection"]
I --> K["JWT Configuration"]
```

**Diagram sources**
- [docker-compose.yml:3-23](file://docker-compose.yml#L3-L23)
- [Dockerfile:1-10](file://Dockerfile#L1-L10)

### Docker Environment Management
- **Environment File Loading**: Application service loads .env.docker via env_file directive
- **Service Dependencies**: Application waits for database service to start
- **Port Configuration**: Application exposes port 8000, database exposes port 5432
- **Credential Standardization**: Both services use 'postgres'/'postgres' credentials

### Docker Build Process
1. **Base Image**: Python 3.13 slim container
2. **Dependencies**: Installs requirements from requirements.txt
3. **Application Code**: Copies application code into container
4. **Command Execution**: Starts Uvicorn server with PORT environment variable support

**Section sources**
- [docker-compose.yml:3-23](file://docker-compose.yml#L3-L23)
- [Dockerfile:1-10](file://Dockerfile#L1-L10)

## Version Control Configuration

### Environment File Exclusion
The repository includes comprehensive version control configuration to prevent sensitive environment files from being committed:

```mermaid
graph LR
A[".gitignore"] --> B["Generated Files"]
B --> C["__pycache__/"]
B --> D["*.py[oc]"]
B --> E["build/"]
B --> F["dist/"]
B --> G["wheels/"]
B --> H["*.egg-info"]
B --> I["arms_cache/"]
A --> J["Environment Files"]
J --> K[".env"]
J --> L[".env.docker"]
```

**Diagram sources**
- [.gitignore:1-15](file://.gitignore#L1-L15)

### Environment File Management
- **Local Development**: .env file for local environment variables
- **Docker Deployment**: .env.docker file for containerized environment variables
- **Template Files**: .env.example and .env.docker.example for configuration templates
- **Exclusion Rules**: Both .env and .env.docker files are excluded from version control

### Best Practices for Environment Management
- **Never Commit**: Never commit .env or .env.docker files to version control
- **Template Usage**: Always copy template files (.example) to actual environment files
- **Secret Rotation**: Regularly rotate SECRET_KEY and SECRET values
- **Environment Separation**: Use separate environment files for different deployment contexts

**Section sources**
- [.gitignore:13-15](file://.gitignore#L13-L15)

## Security Configuration

### Production Deployment Guidelines
1. **Key Generation**: Generate cryptographically secure random keys using appropriate key lengths
2. **Separate Keys**: Use different keys for password hashing and JWT signing
3. **Environment Isolation**: Store keys in separate environment variable stores
4. **Regular Rotation**: Implement scheduled key rotation policies
5. **Access Control**: Restrict key access to authorized personnel only
6. **Template Security**: Ensure template files (.example) are never committed to repositories

### Security Recommendations
- **SECRET_KEY**: Minimum 32 characters, preferably 64+ characters
- **SECRET**: Match SECRET_KEY length requirements for equivalent security
- **DATABASE_URL**: Use SSL connections in production environments
- **Algorithm Selection**: Consider RS256 for distributed systems requiring key distribution
- **Token Lifetimes**: Balance usability with security requirements
- **BASE_URL Security**: Ensure BASE_URL uses HTTPS in production environments

**Section sources**
- [README.md:341-348](file://README.md#L341-L348)

## Configuration Best Practices

### Development Setup Workflow
1. **Clone Repository**: Download the authentication service codebase
2. **Install Dependencies**: Use uv package manager to install requirements
3. **Create Environment Files**: Copy template files to actual environment files
4. **Configure Variables**: Edit .env for local development or .env.docker for Docker
5. **Test Configuration**: Verify service initialization and database connectivity

### Environment File Configuration Examples

**Local Development .env Configuration**
```env
# Application Configuration
BASE_URL="http://localhost:8000"

# Database Configuration
DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/auth_db"

# Security Configuration
SECRET_KEY="your-super-secret-key-change-this-in-production"
SECRET="your-jwt-secret-key-change-this-in-production"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
```

**Docker Deployment .env.docker Configuration**
```env
# Application Configuration
BASE_URL="http://localhost:8000"

# Database Configuration
DATABASE_URL="postgresql+asyncpg://postgres:postgres@db:5432/auth_db"

# Security Configuration
SECRET_KEY="your-super-secret-key-change-this-in-production"
SECRET="your-jwt-secret-key-change-this-in-production"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### Production Hardening
- Use environment-specific key management systems
- Implement key derivation functions for enhanced security
- Regular security audits of configuration management
- Monitor for unauthorized configuration changes
- Implement CI/CD pipeline for environment variable validation

**Section sources**
- [README.md:53-64](file://README.md#L53-L64)
- [README.md:341-348](file://README.md#L341-L348)

## Troubleshooting Guide

### Common Configuration Issues

#### Missing BASE_URL Environment Variable
- **Symptom**: Email verification links show incorrect URLs or application redirects fail
- **Solution**: Set BASE_URL to match your deployment domain and port
- **Example**: `BASE_URL="https://yourdomain.com"` for production

#### Database Connection Failures
- **Symptom**: Database engine creation errors or connection timeouts
- **Solution**: Verify DATABASE_URL format and accessibility
- **Local Fix**: Ensure PostgreSQL is running on localhost:5432
- **Docker Fix**: Ensure database service is running and reachable as 'db'

#### Missing SECRET Environment Variable
- **Symptom**: `RuntimeError: SECRET environment variable is required`
- **Solution**: Set SECRET environment variable with valid key value
- **Security Note**: Use cryptographically secure random values

#### Missing SECRET_KEY Environment Variable
- **Symptom**: Password hashing failures or service initialization errors
- **Solution**: Configure SECRET_KEY for Argon2 operations
- **Security Note**: Use minimum 32 characters for production

#### Environment File Loading Issues
- **Symptom**: Variables not being loaded despite proper configuration
- **Solution**: Verify .env or .env.docker file exists and is readable
- **Check**: Ensure file permissions allow reading by the application process

#### Docker Environment Variable Issues
- **Symptom**: Application fails to start in Docker containers
- **Solution**: Verify .env.docker.example is copied to .env.docker
- **Check**: Ensure docker-compose.yml references correct environment file
- **Debug**: Use `docker-compose logs app` to view application startup errors

### Verification Steps
1. Confirm environment variables are loaded by checking service initialization
2. Test password hashing with HashService.hash_password()
3. Verify JWT token creation with JwtService.createAccessToken()
4. Validate database connectivity with engine test queries
5. Check BASE_URL configuration for proper email verification links
6. Verify Docker environment file loading with container logs

**Section sources**
- [jwt_service.py:14](file://app/services/jwt_service.py#L14)
- [hash_service.py:7](file://app/services/hash_service.py#L7)
- [db.py:16](file://app/config/db.py#L16)

## Conclusion
The authentication service configuration system now provides comprehensive environment variable management through template files, BASE_URL support for email verification, and standardized database credentials. The enhanced system offers improved security through proper environment variable separation, flexible deployment options through Docker integration, and robust configuration management with proper version control practices. The transition from 'admin'/'admin' to 'postgres'/'postgres' credentials aligns with PostgreSQL best practices and improves security posture.

Following the best practices and security recommendations outlined in this document will help ensure secure and reliable operation of the authentication service across development, Docker, and production environments with proper BASE_URL configuration for email verification and application redirects.

## Appendices

### Complete Configuration Examples

#### Environment Variable Templates
**.env.example Template**
```env
# Application Configuration
BASE_URL="http://localhost:8000"

# Database Configuration
DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/auth_db"

# Security Configuration
SECRET_KEY="your-super-secret-key-change-this-in-production"
SECRET="your-jwt-secret-key-change-this-in-production"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
```

**.env.docker.example Template**
```env
# Application Configuration
BASE_URL="http://localhost:8000"

# Database Configuration
DATABASE_URL="postgresql+asyncpg://postgres:postgres@db:5432/auth_db"

# Security Configuration
SECRET_KEY="your-super-secret-key-change-this-in-production"
SECRET="your-jwt-secret-key-change-this-in-production"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
```

#### Production Key Generation
```bash
# Generate secure keys using Python
python3 -c "import secrets; print(secrets.token_urlsafe(64))"
```

### Service Integration Examples
- **HashService**: Used for password registration and verification with Argon2
- **JwtService**: Handles authentication token lifecycle with configurable expiration
- **Database Engine**: Manages async database connections with proper BASE_URL integration
- **Email Verification**: Uses BASE_URL for generating verification links

### Version Control Best Practices
- **Exclude Generated Files**: Always include cache directories in .gitignore
- **Never Commit Secrets**: Ensure .env and .env.docker files are excluded from version control
- **Template Usage**: Always use .example files as templates, never commit them directly
- **Repository Cleanliness**: Keep repository free from generated artifacts and secrets
- **Team Collaboration**: Ensure all team members follow the same exclusion and template rules
- **Build Integrity**: Maintain clean build processes by excluding cached files and secrets

**Section sources**
- [README.md:53-64](file://README.md#L53-L64)
- [README.md:325-340](file://README.md#L325-L340)
- [hash_service.py:10-14](file://app/services/hash_service.py#L10-L14)
- [jwt_service.py:17-32](file://app/services/jwt_service.py#L17-L32)
- [.gitignore:13-15](file://.gitignore#L13-L15)
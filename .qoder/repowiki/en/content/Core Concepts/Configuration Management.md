# Configuration Management

<cite>
**Referenced Files in This Document**
- [jwt_service.py](file://app/services/jwt_service.py)
- [hash_service.py](file://app/services/hash_service.py)
- [db.py](file://app/config/db.py)
- [main.py](file://main.py)
- [.gitignore](file://.gitignore)
- [README.md](file://README.md)
</cite>

## Update Summary
**Changes Made**
- Updated version control section to document the addition of `arms_cache/` directory exclusion to .gitignore
- Enhanced environment variable management documentation with comprehensive reference table
- Added security configuration best practices for production deployments
- Expanded troubleshooting guide with specific configuration issue resolutions
- Updated project structure documentation to reflect current repository organization

## Table of Contents
1. [Introduction](#introduction)
2. [Project Structure](#project-structure)
3. [Core Components](#core-components)
4. [Architecture Overview](#architecture-overview)
5. [Detailed Component Analysis](#detailed-component-analysis)
6. [Environment Variable Management](#environment-variable-management)
7. [Version Control Configuration](#version-control-configuration)
8. [Security Configuration](#security-configuration)
9. [Configuration Best Practices](#configuration-best-practices)
10. [Troubleshooting Guide](#troubleshooting-guide)
11. [Conclusion](#conclusion)
12. [Appendices](#appendices)

## Introduction
This document explains the authentication service configuration management system with a focus on environment variable handling, security considerations, and version control best practices. The system has been updated to separate SECRET_KEY (password hashing) from SECRET (JWT signing), providing enhanced security isolation between different cryptographic operations. Additionally, the repository now includes proper version control configuration to maintain clean separation between generated cache files and source code.

Key aspects covered:
- Environment variable loading and precedence
- Security-conscious configuration separation
- Version control best practices for generated files
- Production-ready deployment guidelines
- Troubleshooting common configuration issues

## Project Structure
The configuration system centers around three primary security-related environment variables managed through dedicated service classes, with proper version control separation:

```mermaid
graph TB
A["Environment Variables"] --> B["SECRET_KEY<br/>(Password Hashing)")
A --> C["SECRET<br/>(JWT Signing)")
A --> D["ALGORITHM<br/>(JWT Algorithm)")
B --> E["HashService"]
C --> F["JwtService"]
E --> G["Password Hashing<br/>(Argon2)"]
F --> H["JWT Token Generation<br/>(HS256)"]
I["Database Configuration"] --> J["DATABASE_URL"]
J --> K["SQLAlchemy Async Engine"]
L[".gitignore<br/>Generated Files Exclusion"] --> M["arms_cache/<br/>Cache Directory"]
M --> N["Generated Cache Files"]
```

**Diagram sources**
- [jwt_service.py:9-14](file://app/services/jwt_service.py#L9-L14)
- [hash_service.py:7](file://app/services/hash_service.py#L7)
- [db.py:9](file://app/config/db.py#L9)
- [.gitignore:8](file://.gitignore#L8)

**Section sources**
- [jwt_service.py:9-14](file://app/services/jwt_service.py#L9-L14)
- [hash_service.py:7](file://app/services/hash_service.py#L7)
- [db.py:9](file://app/config/db.py#L9)
- [.gitignore:8](file://.gitignore#L8)

## Core Components
The configuration system consists of three main security-focused components with proper environment variable separation:

### HashService
Handles password hashing using Argon2 with SECRET_KEY for cryptographic operations. Uses passlib's CryptContext for memory-hard password hashing resistant to GPU attacks.

### JwtService  
Manages JWT token creation and validation using SECRET for signing operations. Supports configurable algorithms (default HS256) and token expiration policies.

### Database Configuration
Manages database connection through DATABASE_URL environment variable with SQLAlchemy async engine configuration.

**Section sources**
- [hash_service.py:6-14](file://app/services/hash_service.py#L6-L14)
- [jwt_service.py:8-38](file://app/services/jwt_service.py#L8-L38)
- [db.py:1-27](file://app/config/db.py#L1-L27)

## Architecture Overview
The configuration pipeline follows a strict security-first approach with environment variable precedence and validation, integrated with proper version control practices:

```mermaid
sequenceDiagram
participant Env as "Environment Variables"
participant Git as ".gitignore"
participant Loader as "dotenv.load_dotenv()"
participant Hash as "HashService"
participant JWT as "JwtService"
participant DB as "Database Config"
Env->>Git : Generated cache files excluded
Git->>Loader : arms_cache/ ignored
Loader->>Hash : SECRET_KEY for Argon2
Loader->>JWT : SECRET for JWT signing
Loader->>DB : DATABASE_URL for connection
Hash->>Hash : Initialize CryptContext
JWT->>JWT : Validate SECRET presence
DB->>DB : Create async engine
```

**Diagram sources**
- [hash_service.py:5](file://app/services/hash_service.py#L5)
- [jwt_service.py:13](file://app/services/jwt_service.py#L13)
- [db.py:7](file://app/config/db.py#L7)
- [.gitignore:8](file://.gitignore#L8)

## Detailed Component Analysis

### Environment Variable Loading
Both HashService and JwtService utilize python-dotenv for secure environment variable loading. The system automatically loads variables from .env files located in the project root, with proper validation and error handling.

### HashService Configuration
- **SECRET_KEY**: Required for Argon2 password hashing operations
- **Cryptographic Context**: Uses passlib's CryptContext with argon2 scheme
- **Memory Hardening**: Configured for resistance against GPU-based attacks

### JwtService Configuration  
- **SECRET**: Required for JWT token signing operations
- **ALGORITHM**: Optional parameter (default HS256)
- **Token Expiration**: Configurable access and refresh token lifetimes
- **Validation**: Runtime validation ensures SECRET is present

### Database Configuration
- **DATABASE_URL**: Required for async PostgreSQL connection
- **Schema Management**: Default schema set to "auth"
- **Connection Pooling**: SQLAlchemy async engine with statement cache disabled

**Section sources**
- [hash_service.py:5-8](file://app/services/hash_service.py#L5-L8)
- [jwt_service.py:9-14](file://app/services/jwt_service.py#L9-L14)
- [db.py:7-9](file://app/config/db.py#L7-L9)

## Environment Variable Management

### Current Environment Variables
| Variable | Description | Default | Required | Security Level |
|----------|-------------|---------|----------|----------------|
| `DATABASE_URL` | PostgreSQL async connection string | `postgresql+asyncpg://admin:admin@localhost:5432/auth_db` | Yes | High |
| `SECRET_KEY` | Secret key for password hashing (Argon2) | - | Yes | Critical |
| `SECRET` | Secret key for JWT signing | - | Yes | Critical |
| `ALGORITHM` | JWT signing algorithm | `HS256` | No | Medium |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token expiration (minutes) | `15` | No | Low |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Refresh token expiration (days) | `7` | No | Low |

### Variable Separation Benefits
The separation of SECRET_KEY and SECRET provides:
- **Security Isolation**: Different cryptographic operations use distinct keys
- **Attack Surface Reduction**: Compromise of one key doesn't affect the other
- **Compliance Support**: Meets security standards requiring key separation
- **Operational Flexibility**: Independent key rotation strategies

**Section sources**
- [README.md:236-245](file://README.md#L236-L245)

## Version Control Configuration

### Generated Files Exclusion
The repository includes proper version control configuration to maintain clean separation between generated cache files and source code:

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
I --> J["Cache Files"]
I --> K["Generated Artifacts"]
```

**Diagram sources**
- [.gitignore:1-8](file://.gitignore#L1-L8)

### arms_cache/ Directory Exclusion
The newly added `arms_cache/` directory exclusion serves several important purposes:
- **Clean Repository**: Prevents generated cache files from cluttering the repository
- **Performance**: Reduces repository size by excluding large cache directories
- **Collaboration**: Ensures team members don't accidentally commit generated files
- **Build Integrity**: Maintains clean build processes by excluding cached artifacts

### Best Practices for Generated Files
- **Cache Directories**: Always exclude `__pycache__/`, `*.pyc`, and `*.pyo`
- **Build Artifacts**: Exclude `build/`, `dist/`, `wheels/`, and `*.egg-info`
- **IDE Cache**: Exclude IDE-specific cache directories
- **Custom Cache**: Use `arms_cache/` for application-specific caching needs

**Section sources**
- [.gitignore:1-8](file://.gitignore#L1-L8)

## Security Configuration

### Production Deployment Guidelines
1. **Key Generation**: Generate cryptographically secure random keys using appropriate key lengths
2. **Separate Keys**: Use different keys for password hashing and JWT signing
3. **Environment Isolation**: Store keys in separate environment variable stores
4. **Regular Rotation**: Implement scheduled key rotation policies
5. **Access Control**: Restrict key access to authorized personnel only

### Security Recommendations
- **SECRET_KEY**: Minimum 32 characters, preferably 64+ characters
- **SECRET**: Match SECRET_KEY length requirements for equivalent security
- **DATABASE_URL**: Use SSL connections in production environments
- **Algorithm Selection**: Consider RS256 for distributed systems requiring key distribution
- **Token Lifetimes**: Balance usability with security requirements

**Section sources**
- [README.md:247-252](file://README.md#L247-L252)

## Configuration Best Practices

### Development Setup
1. Create `.env` file in project root
2. Configure SECRET_KEY for password hashing
3. Configure SECRET for JWT signing
4. Set appropriate token expiration values
5. Test configuration loading with service initialization

### Testing Configuration
```bash
# Development example
SECRET_KEY="dev-secret-key-for-testing-only"
SECRET="jwt-secret-key-for-testing-only"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=1
```

### Production Hardening
- Use environment-specific key management systems
- Implement key derivation functions for enhanced security
- Regular security audits of configuration management
- Monitor for unauthorized configuration changes

**Section sources**
- [README.md:220-234](file://README.md#L220-L234)

## Troubleshooting Guide

### Common Configuration Issues
1. **Missing SECRET Environment Variable**
   - Symptom: `RuntimeError: SECRET environment variable is required`
   - Solution: Set SECRET environment variable with valid key value

2. **Missing SECRET_KEY Environment Variable**
   - Symptom: Password hashing failures or service initialization errors
   - Solution: Configure SECRET_KEY for Argon2 operations

3. **Database Connection Failures**
   - Symptom: Database engine creation errors
   - Solution: Verify DATABASE_URL format and accessibility

4. **JWT Algorithm Errors**
   - Symptom: JWT encoding/decoding failures
   - Solution: Ensure ALGORITHM matches between services and clients

5. **Generated Files Clutter**
   - Symptom: Large repository size or IDE warnings about cache files
   - Solution: Ensure `arms_cache/` directory is properly excluded in .gitignore

### Verification Steps
1. Confirm environment variables are loaded by checking service initialization
2. Test password hashing with HashService.hash_password()
3. Verify JWT token creation with JwtService.createAccessToken()
4. Validate database connectivity with engine test queries
5. Check .gitignore configuration for proper cache file exclusion

**Section sources**
- [jwt_service.py:13](file://app/services/jwt_service.py#L13)
- [hash_service.py:7](file://app/services/hash_service.py#L7)
- [db.py:16](file://app/config/db.py#L16)

## Conclusion
The authentication service configuration system now provides enhanced security through proper environment variable separation and comprehensive security guidance. The distinction between SECRET_KEY (password hashing) and SECRET (JWT signing) enables better security practices, compliance with security standards, and more flexible operational deployments. Additionally, the proper version control configuration with `arms_cache/` directory exclusion ensures clean repository organization and maintains separation between generated cache files and source code.

Following the best practices and security recommendations outlined in this document will help ensure secure and reliable operation of the authentication service across development, staging, and production environments.

## Appendices

### Configuration Examples

#### Complete .env Configuration
```env
# Database Configuration
DATABASE_URL="postgresql+asyncpg://admin:admin@localhost:5432/auth_db"

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
- **HashService**: Used for password registration and verification
- **JwtService**: Handles authentication token lifecycle
- **Database Engine**: Manages async database connections with proper configuration

### Version Control Best Practices
- **Exclude Generated Files**: Always include cache directories in .gitignore
- **Repository Cleanliness**: Keep repository free from generated artifacts
- **Team Collaboration**: Ensure all team members follow the same exclusion rules
- **Build Integrity**: Maintain clean build processes by excluding cached files

**Section sources**
- [README.md:220-234](file://README.md#L220-L234)
- [hash_service.py:10-14](file://app/services/hash_service.py#L10-L14)
- [jwt_service.py:16-31](file://app/services/jwt_service.py#L16-L31)
- [.gitignore:1-8](file://.gitignore#L1-L8)
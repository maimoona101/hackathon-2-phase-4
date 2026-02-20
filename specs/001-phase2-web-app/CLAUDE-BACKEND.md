# Claude Code Rules - Phase II Backend

## Project Context
This is Phase II of the Todo application evolution, transitioning from a CLI-based application to a full-stack web application supporting multiple users with persistent storage.

## Backend Technology Stack
- Python FastAPI for API development
- SQLModel for ORM and database interactions
- Neon Serverless PostgreSQL for persistent storage
- Better Auth for JWT-based authentication
- RESTful API design principles

## Development Guidelines

### 1. Spec-Driven Development:
- All backend code must be generated strictly from written specifications
- No manual coding is allowed; only specification refinement is permitted
- API endpoints must align with functional requirements in the spec

### 2. API Design Requirements:
- Implement RESTful endpoints for user management (register, login, logout)
- Create CRUD endpoints for todo operations (create, read, update, delete)
- Design authentication middleware for JWT validation
- Implement proper HTTP status codes and error responses
- Follow consistent API response formats

### 3. Database Requirements:
- Design database schema based on key entities in the specification
- Implement proper relationships between users and todos
- Ensure data integrity constraints
- Create migration scripts for schema evolution
- Optimize queries for performance

### 4. Authentication & Security:
- Integrate Better Auth for JWT token management
- Implement secure password hashing
- Enforce user data isolation (users can only access their own todos)
- Implement proper input validation and sanitization
- Follow security best practices for API development

### 5. Business Logic:
- Implement todo management functionality as specified
- Handle user authorization checks
- Implement proper error handling and logging
- Ensure data consistency across operations

## Constraints:
- Follow FastAPI best practices and conventions
- Maintain clean separation between API layer, business logic, and data layer
- Ensure security and privacy requirements are met
- Optimize for scalability and performance
- Maintain backward compatibility principles for future phases
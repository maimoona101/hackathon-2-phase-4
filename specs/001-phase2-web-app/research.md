# Research Document: Phase II Todo Web Application

## Overview
This document consolidates research findings for the Phase II Todo web application, addressing technical decisions and best practices for the full-stack implementation.

## Neon PostgreSQL Integration with SQLModel

### Decision
Use SQLModel with async PostgreSQL driver (asyncpg) for Neon integration.

### Rationale
- SQLModel provides seamless integration with both SQLAlchemy and Pydantic
- Async support enables better performance for web applications
- Neon's serverless features work well with connection pooling
- Strong typing support reduces runtime errors

### Alternatives Considered
- Raw SQLAlchemy: Less type safety, more boilerplate
- Tortoise ORM: Good async support but less mature ecosystem
- Databases + SQLAlchemy Core: Less ORM functionality

## Better Auth Integration with FastAPI

### Decision
Integrate Better Auth as the primary authentication provider with JWT tokens.

### Rationale
- Better Auth provides secure, production-ready authentication
- Built-in JWT management and refresh token handling
- Easy integration with FastAPI using dependencies
- Good documentation and community support
- Supports social login extensions if needed

### Implementation Pattern
- Use Better Auth middleware for token validation
- Create custom dependency for user context injection
- Implement role-based access control if needed in future phases

## Next.js App Router Authentication Patterns

### Decision
Use a combination of server-side rendering for protected routes and client-side token management.

### Rationale
- App Router provides better SEO and performance
- Server-side authentication checks prevent unauthorized access
- Client-side token management for dynamic UI updates
- Middleware for route protection

### Implementation Pattern
- Create `(auth)` route group for authentication flows
- Use server actions for authenticated API calls
- Implement loading and error boundaries
- Store tokens securely in httpOnly cookies or secure localStorage

## JWT Token Management Between Frontend and Backend

### Decision
Use httpOnly cookies for JWT storage with automatic refresh mechanisms.

### Rationale
- httpOnly cookies prevent XSS attacks
- Automatic inclusion in requests simplifies frontend code
- Refresh token rotation enhances security
- Better user experience with seamless sessions

### Implementation Pattern
- Backend sets httpOnly cookies with JWT
- Frontend uses fetch interceptors for token management
- Implement silent refresh before token expiration
- Handle token invalidation on logout

## Monorepo Structure for Full-Stack Development

### Decision
Use a clear separation between frontend and backend with shared tooling configuration.

### Rationale
- Clear boundaries between frontend and backend responsibilities
- Shared linting, formatting, and CI/CD tooling
- Simplified dependency management
- Easier collaboration between frontend and backend teams

### Structure Pattern
- src/frontend/: Next.js application with components, pages, etc.
- src/backend/: FastAPI application with API, models, etc.
- Shared configuration files at root level
- Separate package.json/pyproject.toml for each part

## Database Migration Strategy

### Decision
Use Alembic for SQLModel-based database migrations with Neon-compatible patterns.

### Rationale
- Alembic is the standard for SQLAlchemy-based applications
- Works seamlessly with SQLModel
- Supports Neon's serverless features
- Provides rollback capabilities

### Implementation Pattern
- Generate migrations from model changes
- Test migrations in development environment
- Use environment-specific migration configurations
- Implement backup strategies for production

## API Error Handling Standard

### Decision
Implement consistent error response format across all API endpoints.

### Rationale
- Consistent error handling improves frontend reliability
- Standardized format enables better error reporting
- Easier debugging and monitoring
- Better user experience with clear error messages

### Error Format
```json
{
  "success": false,
  "error": {
    "message": "Descriptive error message",
    "code": "ERROR_CODE",
    "details": {} // Optional additional details
  }
}
```

## Frontend State Management

### Decision
Use React Context for authentication state with local component state for UI interactions.

### Rationale
- Context provides global access to authentication state
- Local state keeps UI interactions performant
- Simpler than Redux for this application size
- Native React solution with good performance

### Pattern
- Global AuthContext for user session management
- Local component state for form inputs and UI interactions
- Custom hooks for common state patterns
- Server Actions for data mutations

## Performance Optimization Strategy

### Decision
Implement code splitting, caching, and lazy loading for optimal performance.

### Rationale
- Essential for good user experience
- Reduces initial bundle size
- Improves Core Web Vitals scores
- Better SEO with faster loading pages

### Implementation
- Dynamic imports for heavy components
- Next.js Image optimization
- API response caching
- Database query optimization with proper indexing
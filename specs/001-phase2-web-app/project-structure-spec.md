# Project Structure Specification - Phase II Todo Application

## Overview
This document specifies the monorepo layout and organization for the full-stack web application supporting both frontend (Next.js) and backend (FastAPI) components.

## Monorepo Structure

```
project-root/
├── .specify/                          # Spec-Kit Plus configuration
│   ├── memory/
│   ├── scripts/
│   │   └── powershell/
│   └── templates/
├── specs/                            # All feature specifications
│   └── 001-phase2-web-app/          # Current feature specs
│       ├── spec.md
│       ├── crud-spec.md
│       ├── api-endpoints-spec.md
│       ├── database-schema-spec.md
│       ├── authentication-spec.md
│       ├── project-structure-spec.md
│       ├── CLAUDE-FRONTEND.md
│       ├── CLAUDE-BACKEND.md
│       └── checklists/
├── src/                              # Source code
│   ├── frontend/                     # Next.js application
│   │   ├── app/                      # App Router structure
│   │   │   ├── (auth)/              # Authentication routes
│   │   │   │   ├── login/
│   │   │   │   └── register/
│   │   │   ├── dashboard/            # Main dashboard
│   │   │   ├── todos/                # Todo management
│   │   │   │   ├── page.tsx
│   │   │   │   ├── [id]/             # Individual todo
│   │   │   │   └── components/
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx
│   │   │   └── globals.css
│   │   ├── components/               # Reusable UI components
│   │   │   ├── ui/                  # Base components (buttons, inputs, etc.)
│   │   │   ├── auth/                # Authentication components
│   │   │   └── todos/               # Todo-specific components
│   │   ├── lib/                     # Utility functions and services
│   │   │   ├── api.ts              # API client and service functions
│   │   │   ├── auth.ts             # Authentication utilities
│   │   │   └── utils.ts            # General utilities
│   │   ├── public/                  # Static assets
│   │   ├── styles/                  # Global styles
│   │   ├── types/                   # TypeScript type definitions
│   │   ├── hooks/                   # Custom React hooks
│   │   ├── middleware.ts           # Next.js middleware
│   │   └── package.json
│   └── backend/                     # FastAPI application
│       ├── app/                     # Main application code
│       │   ├── main.py             # Application factory and routing
│       │   ├── api/                # API route definitions
│       │   │   ├── deps.py         # Dependency injection utilities
│       │   │   ├── v1/             # Version 1 API endpoints
│       │   │   │   ├── __init__.py
│       │   │   │   ├── auth.py     # Authentication endpoints
│       │   │   │   ├── todos.py    # Todo endpoints
│       │   │   │   └── users.py    # User endpoints
│       │   ├── models/             # SQLModel database models
│       │   │   ├── __init__.py
│       │   │   ├── user.py         # User model
│       │   │   ├── todo.py         # Todo model
│       │   │   └── session.py      # Session model
│       │   ├── schemas/            # Pydantic request/response schemas
│       │   │   ├── __init__.py
│       │   │   ├── auth.py         # Authentication schemas
│       │   │   ├── todo.py         # Todo schemas
│       │   │   └── user.py         # User schemas
│       │   ├── database/           # Database connection and session management
│       │   │   ├── __init__.py
│       │   │   ├── session.py      # Database session utilities
│       │   │   └── init_db.py      # Database initialization
│       │   ├── auth/               # Authentication logic
│       │   │   ├── __init__.py
│       │   │   ├── jwt_handler.py  # JWT token handling
│       │   │   └── security.py     # Security utilities
│       │   └── core/               # Core application configuration
│       │       ├── __init__.py
│       │       ├── config.py       # Configuration settings
│       │       └── exceptions.py   # Custom exception handlers
│       ├── tests/                  # Backend test suite
│       │   ├── conftest.py         # Test configuration
│       │   ├── test_auth.py        # Authentication tests
│       │   ├── test_todos.py       # Todo functionality tests
│       │   └── test_users.py       # User management tests
│       ├── alembic/                # Database migrations
│       │   ├── versions/           # Migration files
│       │   ├── env.py
│       │   ├── script.py.mako
│       │   └──.ini
│       ├── requirements.txt        # Python dependencies
│       └── alembic.ini            # Alembic configuration
├── history/                        # Project history and records
│   ├── prompts/                    # Prompt history records
│   │   └── 001-phase2-web-app/   # Feature-specific prompts
│   └── adr/                       # Architecture decision records
├── docs/                          # Documentation
│   ├── getting-started.md
│   ├── api-reference.md
│   └── deployment.md
├── .env.example                   # Environment variables template
├── docker-compose.yml             # Docker configuration
├── README.md                      # Project overview
├── package.json                   # Root package file (for shared scripts)
└── CLAUDE.md                      # Claude Code project rules
```

## Frontend Structure (Next.js 16+ with App Router)

### App Directory Structure
- **Route Groups**: `(auth)` for authentication-related routes, keeping them separate from main app
- **Layout System**: Nested layouts with root layout providing global structure
- **Client Components**: Interactive components using 'use client' directive
- **Server Components**: Data-fetching components using server-side rendering

### Component Organization
- **Base Components**: Located in `components/ui/` for primitive UI elements
- **Domain Components**: Located in `components/auth/` and `components/todos/` for feature-specific UI
- **Hooks**: Custom React hooks in `hooks/` directory for shared logic
- **Type Definitions**: TypeScript interfaces and types in `types/` directory

### API Integration
- **Service Layer**: Centralized API client in `lib/api.ts` with axios or fetch wrapper
- **Authentication Utilities**: JWT handling and auth state management in `lib/auth.ts`
- **Error Handling**: Centralized error handling for API responses

## Backend Structure (FastAPI + SQLModel)

### Application Organization
- **Dependency Injection**: Defined in `deps.py` for shared resources like database sessions
- **API Versioning**: v1 namespace for initial API version with room for future versions
- **Model-View-Controller Separation**: Models in `models/`, schemas in `schemas/`, and routes in `api/v1/`

### Database Layer
- **SQLModel Integration**: Combines SQLAlchemy and Pydantic for type-safe database models
- **Migration System**: Alembic for database schema migrations
- **Session Management**: Proper connection pooling and session handling

### Authentication Layer
- **JWT Handling**: Token creation, validation, and refresh mechanisms
- **Better Auth Integration**: Configuration for third-party authentication provider
- **Security Utilities**: Password hashing, input validation, and security middleware

## Development Environment

### Shared Configurations
- **ESLint**: JavaScript/TypeScript linting configuration
- **Prettier**: Code formatting rules
- **TypeScript**: Type checking configuration for frontend
- **Pydantic**: Data validation for backend

### Environment Variables
- **Frontend Variables**: API endpoints, feature flags, analytics keys
- **Backend Variables**: Database URLs, JWT secrets, third-party API keys
- **Shared Variables**: Common configuration values

## Testing Strategy

### Frontend Testing
- **Unit Tests**: Component-level testing with Jest and React Testing Library
- **Integration Tests**: Page and flow testing with Cypress or Playwright
- **Snapshot Tests**: Component rendering consistency

### Backend Testing
- **Unit Tests**: Model and utility function testing
- **Integration Tests**: API endpoint testing with realistic database state
- **Security Tests**: Authentication and authorization validation

## Deployment Configuration

### Containerization
- **Docker Compose**: Multi-container setup for development and production
- **Environment-Specific Configurations**: Separate configs for dev/staging/prod
- **Health Checks**: Application health monitoring endpoints

### Infrastructure as Code
- **Database Setup**: Neon PostgreSQL configuration
- **Environment Variables**: Secure handling of secrets
- **Scaling Configuration**: Resource allocation for different environments

## Reusable Intelligence Structure

### Agent Definitions
- **Planner Agent**: Located in `.specify/agents/planner/` for converting specs to plans
- **Builder Agent**: Located in `.specify/agents/builder/` for implementing plans
- **Reviewer Agent**: Located in `.specify/agents/reviewer/` for validating implementations

### Skill Definitions
- **Task Management Skill**: For todo-related operations
- **Spec Parsing Skill**: For interpreting specifications
- **CLI Interaction Skill**: For command-line interface handling

This structure ensures clear separation of concerns while maintaining the ability to evolve the application through the planned phases while adhering to the spec-driven development methodology.
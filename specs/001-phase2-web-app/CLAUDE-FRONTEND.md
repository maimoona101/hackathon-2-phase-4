# Claude Code Rules - Phase II Frontend

## Project Context
This is Phase II of the Todo application evolution, transitioning from a CLI-based application to a full-stack web application supporting multiple users with persistent storage.

## Frontend Technology Stack
- Next.js 16+ with App Router
- Client-side interaction with REST API
- State management for user interface
- Authentication handling via Better Auth
- Responsive design for multiple device types

## Development Guidelines

### 1. Spec-Driven Development:
- All frontend code must be generated strictly from written specifications
- No manual coding is allowed; only specification refinement is permitted
- Components and pages must be designed based on user scenarios in the spec

### 2. User Interface Requirements:
- Implement responsive design for desktop and mobile
- Create intuitive navigation for todo management
- Design authentication flow (login, registration, logout)
- Implement todo list views with filtering and sorting capabilities
- Ensure accessibility compliance

### 3. Integration Requirements:
- Connect to backend REST API endpoints
- Handle JWT token management for authentication
- Implement error handling for network requests
- Create loading states for asynchronous operations

### 4. Component Architecture:
- Build reusable UI components following Next.js best practices
- Organize components by feature/domain
- Implement proper state management
- Ensure clean separation between presentation and business logic

### 5. Testing and Validation:
- Components must be testable and verifiable against specification requirements
- Implement form validation based on API requirements
- Handle edge cases as defined in the specification

## Constraints:
- Follow Next.js App Router conventions
- Maintain clean separation from backend logic
- Ensure security best practices for client-side applications
- Optimize for performance and user experience
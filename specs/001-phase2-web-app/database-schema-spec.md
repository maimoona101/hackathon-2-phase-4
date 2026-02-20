# Database Schema Specification - Phase II Todo Application

## Overview
This document specifies the database schema for the todo application using Neon Serverless PostgreSQL with SQLModel as the ORM.

## Database Configuration
- **Database**: Neon Serverless PostgreSQL
- **ORM**: SQLModel
- **Connection**: Environment-based configuration with connection pooling

## User Table

### Table: `users`
Stores user account information.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY, NOT NULL, DEFAULT gen_random_uuid() | Unique identifier for the user |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User's email address |
| password_hash | VARCHAR(255) | NOT NULL | Hashed password using secure algorithm |
| display_name | VARCHAR(100) | | User's display name |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Account creation timestamp |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Last update timestamp |

### Indexes:
- `idx_users_email`: UNIQUE INDEX on email column for fast lookups
- `idx_users_created_at`: INDEX on created_at for sorting and filtering

## Todo Table

### Table: `todos`
Stores todo items associated with users.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY, NOT NULL, DEFAULT gen_random_uuid() | Unique identifier for the todo |
| title | VARCHAR(255) | NOT NULL | Title of the todo item |
| description | TEXT | | Detailed description of the todo |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'pending' | Status of the todo: 'pending' or 'completed' |
| priority | VARCHAR(20) | NOT NULL, DEFAULT 'medium' | Priority level: 'low', 'medium', or 'high' |
| user_id | UUID | NOT NULL, FOREIGN KEY | Reference to the owning user |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Creation timestamp |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Last update timestamp |

### Indexes:
- `idx_todos_user_id`: INDEX on user_id for efficient user todo retrieval
- `idx_todos_status`: INDEX on status for filtering by completion status
- `idx_todos_priority`: INDEX on priority for priority-based sorting
- `idx_todos_created_at`: INDEX on created_at for chronological ordering
- `idx_todos_updated_at`: INDEX on updated_at for recency-based queries

### Foreign Key Constraints:
- `fk_todos_user_id`: REFERENCES users(id) with CASCADE DELETE (deleting a user removes all their todos)

## Session Table (for Better Auth integration)

### Table: `sessions`
Stores active user sessions for authentication.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY, NOT NULL, DEFAULT gen_random_uuid() | Unique session identifier |
| user_id | UUID | NOT NULL, FOREIGN KEY | Reference to the user |
| token | VARCHAR(512) | NOT NULL, UNIQUE | JWT token or session identifier |
| expires_at | TIMESTAMP | NOT NULL | Session expiration timestamp |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Session creation timestamp |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Last update timestamp |

### Indexes:
- `idx_sessions_user_id`: INDEX on user_id for user session management
- `idx_sessions_token`: UNIQUE INDEX on token for fast session validation
- `idx_sessions_expires_at`: INDEX on expires_at for cleanup operations

### Foreign Key Constraints:
- `fk_sessions_user_id`: REFERENCES users(id) with CASCADE DELETE

## Schema Relationships

### User-Todo Relationship
- One-to-Many: One user can have many todos
- Relationship: users.id → todos.user_id
- Behavior: When a user is deleted, all their todos are also deleted (CASCADE)

### User-Session Relationship
- One-to-Many: One user can have multiple active sessions
- Relationship: users.id → sessions.user_id
- Behavior: When a user is deleted, all their sessions are also deleted (CASCADE)

## Database Constraints

### Check Constraints:
1. `check_todo_status`: Ensure todo status is either 'pending' or 'completed'
2. `check_todo_priority`: Ensure todo priority is 'low', 'medium', or 'high'
3. `check_email_format`: Validate email format using regex pattern
4. `check_password_strength`: Ensure password meets minimum strength requirements (handled at application level)

### Unique Constraints:
1. `users.email`: Email addresses must be unique across all users
2. `sessions.token`: Session tokens must be unique

## Data Integrity Rules

### Referential Integrity:
- All foreign key relationships enforce referential integrity
- Orphaned records are prevented through foreign key constraints
- CASCADE DELETE ensures data consistency when parent records are removed

### Data Validation:
- Email format validation at database level
- Non-null constraints on required fields
- Length constraints on variable-length fields to prevent oversized data

## Indexing Strategy

### Primary Indexes:
- Automatic primary key indexes on all ID columns
- Optimized for primary key lookups

### Secondary Indexes:
- User lookups by email
- Todo filtering by user, status, and priority
- Session validation by token
- Time-based queries for creation and update timestamps

### Performance Considerations:
- Indexes optimized for common query patterns
- Avoid over-indexing to maintain write performance
- Regular index maintenance through database statistics updates

## Migration Strategy
- Use SQLModel's migration capabilities for schema evolution
- Maintain backward compatibility during schema changes
- Implement zero-downtime migration patterns where possible
- Backup strategy for schema changes in production
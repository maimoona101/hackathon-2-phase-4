# Data Model: Phase II Todo Web Application

## Overview
This document defines the data models for the Phase II Todo web application, specifying entities, relationships, and validation rules.

## User Entity

### Fields
- **id** (UUID, Primary Key)
  - Type: UUID (auto-generated)
  - Constraints: NOT NULL, UNIQUE, DEFAULT gen_random_uuid()
  - Description: Unique identifier for each user

- **email** (VARCHAR)
  - Type: VARCHAR(255)
  - Constraints: NOT NULL, UNIQUE
  - Validation: Valid email format pattern
  - Description: User's email address for login

- **password_hash** (VARCHAR)
  - Type: VARCHAR(255)
  - Constraints: NOT NULL
  - Description: Securely hashed password using bcrypt or similar

- **display_name** (VARCHAR)
  - Type: VARCHAR(100)
  - Constraints: OPTIONAL
  - Description: User's preferred display name

- **created_at** (TIMESTAMP)
  - Type: TIMESTAMP
  - Constraints: NOT NULL, DEFAULT CURRENT_TIMESTAMP
  - Description: Account creation timestamp

- **updated_at** (TIMESTAMP)
  - Type: TIMESTAMP
  - Constraints: NOT NULL, DEFAULT CURRENT_TIMESTAMP
  - Description: Last update timestamp (automatically updated)

### Validation Rules
- Email must be in valid email format
- Email must be unique across all users
- Password must meet minimum strength requirements (handled during registration)
- Display name length between 1 and 100 characters if provided

## Todo Entity

### Fields
- **id** (UUID, Primary Key)
  - Type: UUID (auto-generated)
  - Constraints: NOT NULL, UNIQUE, DEFAULT gen_random_uuid()
  - Description: Unique identifier for each todo item

- **title** (VARCHAR)
  - Type: VARCHAR(255)
  - Constraints: NOT NULL
  - Description: Title of the todo item

- **description** (TEXT)
  - Type: TEXT
  - Constraints: OPTIONAL
  - Description: Detailed description of the todo item

- **status** (VARCHAR)
  - Type: VARCHAR(20)
  - Constraints: NOT NULL, DEFAULT 'pending'
  - Values: 'pending', 'completed'
  - Description: Current status of the todo item

- **priority** (VARCHAR)
  - Type: VARCHAR(20)
  - Constraints: NOT NULL, DEFAULT 'medium'
  - Values: 'low', 'medium', 'high'
  - Description: Priority level of the todo item

- **user_id** (UUID, Foreign Key)
  - Type: UUID
  - Constraints: NOT NULL, FOREIGN KEY REFERENCES users(id)
  - Description: Reference to the user who owns this todo

- **created_at** (TIMESTAMP)
  - Type: TIMESTAMP
  - Constraints: NOT NULL, DEFAULT CURRENT_TIMESTAMP
  - Description: Creation timestamp

- **updated_at** (TIMESTAMP)
  - Type: TIMESTAMP
  - Constraints: NOT NULL, DEFAULT CURRENT_TIMESTAMP
  - Description: Last update timestamp (automatically updated)

### Validation Rules
- Title must not be empty (length > 0)
- Status must be one of the allowed values
- Priority must be one of the allowed values
- User_id must reference an existing user
- User can only access todos they own

## Session Entity

### Fields
- **id** (UUID, Primary Key)
  - Type: UUID (auto-generated)
  - Constraints: NOT NULL, UNIQUE, DEFAULT gen_random_uuid()
  - Description: Unique identifier for each session

- **user_id** (UUID, Foreign Key)
  - Type: UUID
  - Constraints: NOT NULL, FOREIGN KEY REFERENCES users(id)
  - Description: Reference to the user this session belongs to

- **token** (VARCHAR)
  - Type: VARCHAR(512)
  - Constraints: NOT NULL, UNIQUE
  - Description: JWT token or session identifier

- **expires_at** (TIMESTAMP)
  - Type: TIMESTAMP
  - Constraints: NOT NULL
  - Description: Session expiration timestamp

- **created_at** (TIMESTAMP)
  - Type: TIMESTAMP
  - Constraints: NOT NULL, DEFAULT CURRENT_TIMESTAMP
  - Description: Session creation timestamp

- **updated_at** (TIMESTAMP)
  - Type: TIMESTAMP
  - Constraints: NOT NULL, DEFAULT CURRENT_TIMESTAMP
  - Description: Last update timestamp (automatically updated)

### Validation Rules
- Token must be unique across all sessions
- User_id must reference an existing user
- Expires_at must be in the future
- Session is invalid after expiration

## Relationships

### User to Todo (One-to-Many)
- One user can have many todos
- Relationship: users.id → todos.user_id
- Cascade: When user is deleted, all their todos are also deleted
- Constraint: Users can only access their own todos

### User to Session (One-to-Many)
- One user can have multiple active sessions
- Relationship: users.id → sessions.user_id
- Cascade: When user is deleted, all their sessions are also deleted
- Constraint: Sessions must belong to valid users

## State Transitions

### Todo Status Transitions
- **Initial State**: 'pending'
- **Transitions**:
  - 'pending' → 'completed' (when user marks as complete)
  - 'completed' → 'pending' (when user reopens)

### Session Lifecycle
- **Creation**: New session when user logs in successfully
- **Validation**: Check token validity and expiration during each request
- **Deletion**: Session removed when user logs out or token expires

## Indexes

### Users Table
- `idx_users_email`: UNIQUE INDEX on email (for fast login lookup)
- `idx_users_created_at`: INDEX on created_at (for chronological queries)

### Todos Table
- `idx_todos_user_id`: INDEX on user_id (for user-specific todo retrieval)
- `idx_todos_status`: INDEX on status (for filtering by completion status)
- `idx_todos_priority`: INDEX on priority (for priority-based sorting)
- `idx_todos_created_at`: INDEX on created_at (for chronological ordering)
- `idx_todos_updated_at`: INDEX on updated_at (for recency-based queries)

### Sessions Table
- `idx_sessions_user_id`: INDEX on user_id (for user session management)
- `idx_sessions_token`: UNIQUE INDEX on token (for fast session validation)
- `idx_sessions_expires_at`: INDEX on expires_at (for cleanup operations)

## Constraints

### Check Constraints
- `check_todo_status`: Ensure todo.status is either 'pending' or 'completed'
- `check_todo_priority`: Ensure todo.priority is 'low', 'medium', or 'high'

### Foreign Key Constraints
- `fk_todos_user_id`: todos.user_id → users.id (CASCADE DELETE)
- `fk_sessions_user_id`: sessions.user_id → users.id (CASCADE DELETE)

### Unique Constraints
- `users.email`: Email addresses must be unique
- `sessions.token`: Session tokens must be unique

## Data Integrity Rules

### Referential Integrity
- All foreign key relationships enforce referential integrity
- Orphaned records are prevented through foreign key constraints
- CASCADE DELETE ensures data consistency when parent records are removed

### Data Validation
- Email format validation at database level
- Non-null constraints on required fields
- Length constraints on variable-length fields to prevent oversized data
- Enum value validation for status and priority fields
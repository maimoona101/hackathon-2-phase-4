# Data Model: AI-Powered Todo Chatbot

## Entities

### Conversation
- **Fields**:
  - id (UUID, primary key)
  - user_id (integer, foreign key to user table)
  - created_at (timestamp)
  - updated_at (timestamp)
  - metadata (JSONB, for storing conversation context)
- **Relationships**:
  - Belongs to User
  - Has many Messages
- **Validation**:
  - user_id must exist in users table
  - created_at and updated_at are automatically managed
- **State Transitions**:
  - Active (ongoing conversation)
  - Archived (after timeout or user request)

### Message
- **Fields**:
  - id (UUID, primary key)
  - conversation_id (UUID, foreign key to conversation table)
  - role (string: "user", "assistant", "tool")
  - content (text)
  - timestamp (timestamp)
  - tool_calls (JSONB, for storing tool call information)
  - tool_responses (JSONB, for storing tool responses)
- **Relationships**:
  - Belongs to Conversation
- **Validation**:
  - role must be one of the allowed values
  - conversation_id must exist in conversations table
  - content cannot be empty

### ToolExecution
- **Fields**:
  - id (UUID, primary key)
  - conversation_id (UUID, foreign key to conversation table)
  - tool_name (string, name of the tool called)
  - parameters (JSONB, parameters passed to the tool)
  - result (JSONB, result returned by the tool)
  - execution_time (timestamp)
  - success (boolean)
- **Relationships**:
  - Belongs to Conversation
- **Validation**:
  - tool_name must be one of: add_task, list_tasks, update_task, complete_task, delete_task
  - conversation_id must exist in conversations table

### UserSession
- **Fields**:
  - id (UUID, primary key)
  - user_id (integer, foreign key to user table)
  - session_token (string, the authentication token for API calls)
  - created_at (timestamp)
  - expires_at (timestamp)
- **Relationships**:
  - Belongs to User
- **Validation**:
  - user_id must exist in users table
  - session_token must be valid for Phase-2 API
  - expires_at must be in the future

## Relationships
- User (1) → (many) Conversations
- Conversation (1) → (many) Messages
- Conversation (1) → (many) ToolExecutions
- User (1) → (many) UserSessions
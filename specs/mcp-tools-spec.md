# MCP Tools Specification: AI-Powered Todo Chatbot

## Overview

This specification defines the MCP (Model Context Protocol) tools for the AI-powered Todo Chatbot in Phase III. These tools will enable the OpenAI Agent to interact with the existing Phase-2 Todo App backend APIs through natural language commands.

## Tools Specification

### 1. add_task

#### Purpose
Allows the AI agent to create new tasks in the user's todo list through natural language commands.

#### Parameters
- `title` (string, required): The title or description of the task
- `description` (string, optional): Detailed description of the task
- `due_date` (string, optional): Due date for the task in ISO 8601 format (YYYY-MM-DD)

#### Corresponding Phase-2 API Endpoint Mapping
POST `/api/todos/` with JSON payload:
```json
{
  "title": "task title",
  "description": "task description",
  "due_date": "2023-12-31"
}
```

#### Example Input
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread, fruits",
  "due_date": "2026-02-01"
}
```

#### Example Output
```json
{
  "id": 123,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread, fruits",
  "due_date": "2026-02-01",
  "completed": false,
  "created_at": "2026-01-29T10:30:00Z"
}
```

#### Error Handling
- `400 Bad Request`: Missing required parameters or invalid data format
- `401 Unauthorized`: User not authenticated
- `500 Internal Server Error`: Unexpected server error

### 2. list_tasks

#### Purpose
Allows the AI agent to retrieve the user's current todo list to provide status updates or to reference existing tasks.

#### Parameters
- `status` (string, optional): Filter tasks by status ("all", "pending", "completed"). Default: "all"
- `limit` (integer, optional): Maximum number of tasks to return. Default: 100
- `offset` (integer, optional): Number of tasks to skip for pagination. Default: 0

#### Corresponding Phase-2 API Endpoint Mapping
GET `/api/todos/?status={status}&limit={limit}&offset={offset}`

#### Example Input
```json
{
  "status": "pending",
  "limit": 10
}
```

#### Example Output
```json
[
  {
    "id": 121,
    "title": "Prepare presentation",
    "description": "Slides for quarterly review",
    "due_date": "2026-02-05",
    "completed": false,
    "created_at": "2026-01-28T14:20:00Z"
  },
  {
    "id": 122,
    "title": "Call client",
    "description": "Discuss project timeline",
    "due_date": "2026-01-30",
    "completed": false,
    "created_at": "2026-01-29T09:15:00Z"
  }
]
```

#### Error Handling
- `401 Unauthorized`: User not authenticated
- `500 Internal Server Error`: Unexpected server error

### 3. update_task

#### Purpose
Allows the AI agent to modify existing tasks in the user's todo list, including updating title, description, due date, or other attributes.

#### Parameters
- `task_id` (integer, required): Unique identifier of the task to update
- `title` (string, optional): New title for the task
- `description` (string, optional): New description for the task
- `due_date` (string, optional): New due date in ISO 8601 format
- `completed` (boolean, optional): Whether the task is completed

#### Corresponding Phase-2 API Endpoint Mapping
PATCH `/api/todos/{task_id}/` with JSON payload:
```json
{
  "title": "new title",
  "description": "new description",
  "due_date": "2023-12-31",
  "completed": true
}
```

#### Example Input
```json
{
  "task_id": 123,
  "title": "Buy groceries and household items",
  "completed": true
}
```

#### Example Output
```json
{
  "id": 123,
  "title": "Buy groceries and household items",
  "description": "Milk, eggs, bread, fruits",
  "due_date": "2026-02-01",
  "completed": true,
  "created_at": "2026-01-29T10:30:00Z",
  "updated_at": "2026-01-29T11:45:00Z"
}
```

#### Error Handling
- `400 Bad Request`: Invalid data format
- `401 Unauthorized`: User not authenticated
- `404 Not Found`: Task with given ID does not exist
- `500 Internal Server Error`: Unexpected server error

### 4. complete_task

#### Purpose
Allows the AI agent to mark a specific task as completed, updating its status in the todo list.

#### Parameters
- `task_id` (integer, required): Unique identifier of the task to mark as completed

#### Corresponding Phase-2 API Endpoint Mapping
PATCH `/api/todos/{task_id}/` with JSON payload:
```json
{
  "completed": true
}
```

#### Example Input
```json
{
  "task_id": 123
}
```

#### Example Output
```json
{
  "id": 123,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread, fruits",
  "due_date": "2026-02-01",
  "completed": true,
  "created_at": "2026-01-29T10:30:00Z",
  "updated_at": "2026-01-29T12:00:00Z"
}
```

#### Error Handling
- `401 Unauthorized`: User not authenticated
- `404 Not Found`: Task with given ID does not exist
- `500 Internal Server Error`: Unexpected server error

### 5. delete_task

#### Purpose
Allows the AI agent to remove a task from the user's todo list permanently.

#### Parameters
- `task_id` (integer, required): Unique identifier of the task to delete

#### Corresponding Phase-2 API Endpoint Mapping
DELETE `/api/todos/{task_id}/`

#### Example Input
```json
{
  "task_id": 123
}
```

#### Example Output
```json
{
  "success": true,
  "message": "Task deleted successfully"
}
```

#### Error Handling
- `401 Unauthorized`: User not authenticated
- `404 Not Found`: Task with given ID does not exist
- `500 Internal Server Error`: Unexpected server error

## MCP Server Implementation Guidelines

### Authentication
- Each tool call must include the user's authentication token
- The MCP server must validate the token against the existing Phase-2 authentication system
- Tokens should be passed securely through headers or context

### Error Handling Consistency
- All tools must return consistent error structures
- Use HTTP status codes appropriately
- Include meaningful error messages for debugging

### Logging and Monitoring
- Log all tool invocations for debugging and audit purposes
- Monitor tool usage for performance and reliability metrics
- Track success and failure rates for each tool

## Integration with OpenAI Agent

### Tool Schema Format
The MCP tools should be registered with the OpenAI Agent using the following schema format:

```json
{
  "type": "function",
  "function": {
    "name": "add_task",
    "description": "Create a new task in the user's todo list",
    "parameters": {
      "type": "object",
      "properties": {
        "title": {
          "type": "string",
          "description": "The title of the task"
        },
        "description": {
          "type": "string",
          "description": "Detailed description of the task"
        },
        "due_date": {
          "type": "string",
          "description": "Due date for the task in YYYY-MM-DD format"
        }
      },
      "required": ["title"]
    }
  }
}
```

## Security Considerations

- All API calls must be authenticated using existing Phase-2 authentication mechanisms
- Validate user permissions for each operation
- Implement rate limiting to prevent abuse
- Sanitize all input parameters to prevent injection attacks
- Encrypt sensitive data in transit using HTTPS

## Performance Requirements

- Tool response time should be under 2 seconds for 95% of requests
- Support concurrent operations for multiple users
- Implement caching where appropriate for read operations
- Optimize database queries for common operations
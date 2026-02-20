# REST API Endpoints Specification - Phase II Todo Application

## Base URL
All API endpoints are prefixed with `/api`

## Authentication
Most endpoints require JWT authentication in the Authorization header:
```
Authorization: Bearer <jwt_token>
```

## Common Response Format
Successful responses follow this format:
```json
{
  "success": true,
  "data": { /* response data */ },
  "timestamp": "ISO 8601 timestamp"
}
```

Error responses follow this format:
```json
{
  "success": false,
  "error": {
    "message": "Error message",
    "code": "ERROR_CODE",
    "details": { /* optional error details */ }
  },
  "timestamp": "ISO 8601 timestamp"
}
```

## Authentication Endpoints

### Register User
- **POST** `/api/auth/register`
- **Public**: No authentication required
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "securePassword123"
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "data": {
      "message": "Registration successful"
    }
  }
  ```
- **Status Codes**: 201 Created, 400 Bad Request, 409 Conflict

### Login User
- **POST** `/api/auth/login`
- **Public**: No authentication required
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "securePassword123"
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "data": {
      "token": "jwt_token_here",
      "user": {
        "id": "user_id",
        "email": "user@example.com"
      }
    }
  }
  ```
- **Status Codes**: 200 OK, 400 Bad Request, 401 Unauthorized

### Logout User
- **POST** `/api/auth/logout`
- **Protected**: JWT authentication required
- **Response**:
  ```json
  {
    "success": true,
    "data": {
      "message": "Logout successful"
    }
  }
  ```
- **Status Codes**: 200 OK

## Todo Management Endpoints

### Get All Todos
- **GET** `/api/todos`
- **Protected**: JWT authentication required
- **Query Parameters**:
  - `status`: "all", "pending", "completed" (default: "all")
  - `limit`: number (default: 50, max: 100)
  - `offset`: number (default: 0)
  - `sortBy`: "createdAt", "updatedAt", "priority" (default: "createdAt")
  - `sortOrder`: "asc", "desc" (default: "desc")
- **Response**:
  ```json
  {
    "success": true,
    "data": {
      "todos": [
        {
          "id": "todo_id",
          "title": "Todo title",
          "description": "Todo description",
          "status": "pending",
          "priority": "high",
          "userId": "user_id",
          "createdAt": "ISO 8601 timestamp",
          "updatedAt": "ISO 8601 timestamp"
        }
      ],
      "pagination": {
        "total": 100,
        "limit": 50,
        "offset": 0,
        "hasMore": true
      }
    }
  }
  ```
- **Status Codes**: 200 OK

### Create Todo
- **POST** `/api/todos`
- **Protected**: JWT authentication required
- **Request Body**:
  ```json
  {
    "title": "New todo title",
    "description": "Todo description (optional)",
    "priority": "medium" // "low", "medium", "high"
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "data": {
      "id": "new_todo_id",
      "title": "New todo title",
      "description": "Todo description",
      "status": "pending",
      "priority": "medium",
      "userId": "user_id",
      "createdAt": "ISO 8601 timestamp",
      "updatedAt": "ISO 8601 timestamp"
    }
  }
  ```
- **Status Codes**: 201 Created, 400 Bad Request

### Get Single Todo
- **GET** `/api/todos/{id}`
- **Protected**: JWT authentication required
- **Response**:
  ```json
  {
    "success": true,
    "data": {
      "id": "todo_id",
      "title": "Todo title",
      "description": "Todo description",
      "status": "pending",
      "priority": "high",
      "userId": "user_id",
      "createdAt": "ISO 8601 timestamp",
      "updatedAt": "ISO 8601 timestamp"
    }
  }
  ```
- **Status Codes**: 200 OK, 404 Not Found, 403 Forbidden

### Update Todo
- **PUT** `/api/todos/{id}`
- **Protected**: JWT authentication required
- **Request Body** (all optional):
  ```json
  {
    "title": "Updated title",
    "description": "Updated description",
    "status": "completed", // "pending", "completed"
    "priority": "high"
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "data": {
      "id": "todo_id",
      "title": "Updated title",
      "description": "Updated description",
      "status": "completed",
      "priority": "high",
      "userId": "user_id",
      "createdAt": "Original timestamp",
      "updatedAt": "Updated timestamp"
    }
  }
  ```
- **Status Codes**: 200 OK, 400 Bad Request, 404 Not Found, 403 Forbidden

### Delete Todo
- **DELETE** `/api/todos/{id}`
- **Protected**: JWT authentication required
- **Response**:
  ```json
  {
    "success": true,
    "data": {
      "message": "Todo deleted successfully"
    }
  }
  ```
- **Status Codes**: 200 OK, 404 Not Found, 403 Forbidden

## User Profile Endpoints

### Get User Profile
- **GET** `/api/users/profile`
- **Protected**: JWT authentication required
- **Response**:
  ```json
  {
    "success": true,
    "data": {
      "id": "user_id",
      "email": "user@example.com",
      "displayName": "Display Name",
      "createdAt": "ISO 8601 timestamp"
    }
  }
  ```
- **Status Codes**: 200 OK

### Update User Profile
- **PUT** `/api/users/profile`
- **Protected**: JWT authentication required
- **Request Body** (all optional):
  ```json
  {
    "displayName": "New Display Name"
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "data": {
      "id": "user_id",
      "email": "user@example.com",
      "displayName": "New Display Name",
      "updatedAt": "ISO 8601 timestamp"
    }
  }
  ```
- **Status Codes**: 200 OK, 400 Bad Request

## Error Codes
- `VALIDATION_ERROR`: Request validation failed
- `AUTHENTICATION_REQUIRED`: Authentication token missing or invalid
- `FORBIDDEN_ACCESS`: User lacks permission for requested resource
- `RESOURCE_NOT_FOUND`: Requested resource does not exist
- `INTERNAL_SERVER_ERROR`: Unexpected server error occurred
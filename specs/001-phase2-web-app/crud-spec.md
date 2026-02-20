# CRUD Feature Specification - Phase II Todo Application

## Overview
This document outlines the Create, Read, Update, and Delete operations for the todo items and user management in the web application.

## Todo Operations

### Create Todo
- **Endpoint**: POST /api/todos
- **Authorization**: Valid JWT token required
- **Request Body**:
  - title (string, required)
  - description (string, optional)
  - priority (enum: low, medium, high, required, default: medium)
- **Response**: Created todo object with ID, timestamps, and user association
- **Validation**: Title must not be empty, priority must be valid enum value
- **Business Logic**: Associates todo with authenticated user

### Read Todos
- **Endpoint**: GET /api/todos
- **Authorization**: Valid JWT token required
- **Query Parameters**:
  - status (optional, enum: all, pending, completed)
  - limit (optional, integer, default: 50)
  - offset (optional, integer, default: 0)
  - sortBy (optional, enum: createdAt, updatedAt, priority)
  - sortOrder (optional, enum: asc, desc, default: desc)
- **Response**: Paginated list of todos belonging to the authenticated user

### Read Single Todo
- **Endpoint**: GET /api/todos/{todoId}
- **Authorization**: Valid JWT token required
- **Response**: Specific todo object if owned by authenticated user
- **Error Handling**: Return 404 if todo doesn't exist, 403 if not owned by user

### Update Todo
- **Endpoint**: PUT /api/todos/{todoId}
- **Authorization**: Valid JWT token required
- **Request Body** (all optional):
  - title (string)
  - description (string)
  - status (enum: pending, completed)
  - priority (enum: low, medium, high)
- **Response**: Updated todo object
- **Validation**: User must own the todo being updated
- **Business Logic**: Updates updatedAt timestamp

### Delete Todo
- **Endpoint**: DELETE /api/todos/{todoId}
- **Authorization**: Valid JWT token required
- **Response**: Success confirmation
- **Validation**: User must own the todo being deleted
- **Business Logic**: Permanently removes todo from database

## User Operations

### Create User (Register)
- **Endpoint**: POST /api/auth/register
- **Authorization**: None required
- **Request Body**:
  - email (string, required)
  - password (string, required with minimum strength requirements)
- **Response**: Success confirmation or validation errors
- **Validation**: Email must be unique and valid format, password must meet strength requirements

### Read User Profile
- **Endpoint**: GET /api/users/profile
- **Authorization**: Valid JWT token required
- **Response**: User profile information (excluding sensitive data)

### Update User Profile
- **Endpoint**: PUT /api/users/profile
- **Authorization**: Valid JWT token required
- **Request Body** (optional fields):
  - email (string, if allowed to change)
  - displayName (string)
- **Response**: Updated user profile information

### Delete User Account
- **Endpoint**: DELETE /api/users/account
- **Authorization**: Valid JWT token required
- **Response**: Success confirmation
- **Business Logic**: Removes user and all associated todos, invalidates all active sessions

## Error Handling
- All operations must return appropriate HTTP status codes
- Error responses must follow consistent format: { "error": "message", "code": "error_code" }
- Validation errors must include specific field information where applicable
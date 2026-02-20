"""
MCP Tool for listing tasks
This module implements the list_tasks functionality for the AI agent
"""

import asyncio
from typing import Dict, Any, Optional, List
from sqlmodel import Session

from ...models.todo import Todo
from ...services.todo_service import TodoService


class ListTasksTool:
    def __init__(self, session: Session, user_id: str = None):
        self.session = session
        self.user_id = user_id
        self.service = TodoService(session)

    async def execute(self, status: Optional[str] = "all", limit: Optional[int] = 100, offset: Optional[int] = 0) -> List[Dict[str, Any]]:
        """
        Execute the list_tasks tool to retrieve user's tasks
        Maps to existing GET /api/todos/ endpoint functionality
        """
        try:
            # Validate parameters
            if status and status not in ["all", "pending", "completed"]:
                raise ValueError(f"Invalid status: {status}. Valid values are 'all', 'pending', 'completed'")

            if limit and (limit < 1 or limit > 1000):
                raise ValueError("Limit must be between 1 and 1000")

            if offset and offset < 0:
                raise ValueError("Offset must be non-negative")

            # Check if user_id is available
            if not self.user_id:
                raise ValueError("User context is required to list tasks")

            # Use the existing TodoService to get tasks for the specific user
            # Note: The service method signature may need adjustment based on actual implementation
            todos = self.service.get_todos_by_user(
                user_id=self.user_id,
                completed=True if status == "completed" else False if status == "pending" else None,
                limit=limit,
                offset=offset,
                sort_by="created_at",
                sort_order="desc"
            )

            # Transform the todos to the expected format
            result = []
            for todo in todos:
                result.append({
                    "id": str(todo.id),
                    "title": todo.title,
                    "description": todo.description,
                    "due_date": todo.due_date,
                    "completed": todo.status == "completed",
                    "created_at": todo.created_at.isoformat() if todo.created_at else None
                })

            # Log successful execution
            print(f"Successfully retrieved {len(result)} tasks for user {self.user_id}")
            return result
        except ValueError as ve:
            # Handle validation errors
            error_msg = f"Validation error in list_tasks: {str(ve)}"
            print(error_msg)
            raise ve
        except Exception as e:
            # Handle other errors
            error_msg = f"Error in list_tasks tool: {str(e)}"
            print(error_msg)
            # Re-raise with more context for the calling function
            raise e

    def get_tool_definition(self):
        """
        Return the tool definition for OpenAI agent registration
        """
        return {
            "type": "function",
            "function": {
                "name": "list_tasks",
                "description": "Retrieve the user's current todo list with optional filtering",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "status": {
                            "type": "string",
                            "description": "Filter tasks by status: 'all', 'pending', 'completed'. Default: 'all'",
                            "enum": ["all", "pending", "completed"]
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of tasks to return. Default: 100"
                        },
                        "offset": {
                            "type": "integer",
                            "description": "Number of tasks to skip for pagination. Default: 0"
                        }
                    }
                }
            }
        }


# Async wrapper for easier use
async def run_list_tasks(session: Session, user_id: str = None, **kwargs) -> List[Dict[str, Any]]:
    tool = ListTasksTool(session, user_id)
    return await tool.execute(**kwargs)
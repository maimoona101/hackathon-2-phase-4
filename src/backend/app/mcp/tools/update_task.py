"""
MCP Tool for updating tasks
This module implements the update_task functionality for the AI agent
"""

import asyncio
from typing import Dict, Any, Optional
from sqlmodel import Session

from ...models.todo import Todo
from ...schemas.todo import TodoUpdate
from ...services.todo_service import TodoService


class UpdateTaskTool:
    def __init__(self, session: Session, user_id: str = None):
        self.session = session
        self.user_id = user_id
        self.service = TodoService(session)

    async def execute(self, task_id: str, title: Optional[str] = None, description: Optional[str] = None, due_date: Optional[str] = None, completed: Optional[bool] = None) -> Dict[str, Any]:
        """
        Execute the update_task tool to modify an existing task
        Maps to existing PATCH /api/todos/{task_id}/ endpoint functionality
        """
        try:
            # Validate required parameters
            if not task_id or not task_id.strip():
                raise ValueError("Task ID is required and cannot be empty")

            # Additional validation for due_date format if provided
            if due_date:
                from datetime import datetime
                try:
                    datetime.fromisoformat(due_date.replace('Z', '+00:00'))
                except ValueError:
                    raise ValueError(f"Invalid date format for due_date: {due_date}. Expected ISO format (YYYY-MM-DD)")

            # Check if user_id is available
            if not self.user_id:
                raise ValueError("User context is required to update a task")

            # Prepare the update data - only include fields that are provided
            update_data = {}
            if title is not None:
                update_data['title'] = title.strip() if title.strip() else None
            if description is not None:
                update_data['description'] = description.strip() if description else None
            if due_date is not None:
                update_data['due_date'] = due_date
            if completed is not None:
                update_data['status'] = "completed" if completed else "pending"

            # Check if any update data was provided
            if not update_data:
                raise ValueError("At least one field must be provided to update the task")

            # Create TodoUpdate object
            todo_update = TodoUpdate(**update_data)

            # Use the existing TodoService to update the task for the specific user
            updated_todo = self.service.update_todo(task_id, todo_update, self.user_id)

            if not updated_todo:
                raise ValueError(f"Task with ID {task_id} not found or not owned by user")

            # Return the updated task in the expected format
            result = {
                "id": str(updated_todo.id),
                "title": updated_todo.title,
                "description": updated_todo.description,
                "due_date": updated_todo.due_date,
                "completed": updated_todo.status == "completed",
                "created_at": updated_todo.created_at.isoformat() if updated_todo.created_at else None,
                "updated_at": updated_todo.updated_at.isoformat() if hasattr(updated_todo, 'updated_at') and updated_todo.updated_at else None
            }

            # Log successful execution
            print(f"Successfully updated task '{updated_todo.title}' with ID {updated_todo.id}")
            return result
        except ValueError as ve:
            # Handle validation errors
            error_msg = f"Validation error in update_task: {str(ve)}"
            print(error_msg)
            raise ve
        except Exception as e:
            # Handle other errors
            error_msg = f"Error in update_task tool: {str(e)}"
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
                "name": "update_task",
                "description": "Modify an existing task in the user's todo list",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "string",
                            "description": "Unique identifier of the task to update"
                        },
                        "title": {
                            "type": "string",
                            "description": "New title for the task"
                        },
                        "description": {
                            "type": "string",
                            "description": "New description for the task"
                        },
                        "due_date": {
                            "type": "string",
                            "description": "New due date in YYYY-MM-DD format"
                        },
                        "completed": {
                            "type": "boolean",
                            "description": "Whether the task is completed"
                        }
                    },
                    "required": ["task_id"]
                }
            }
        }


# Async wrapper for easier use
async def run_update_task(session: Session, user_id: str = None, **kwargs) -> Dict[str, Any]:
    tool = UpdateTaskTool(session, user_id)
    return await tool.execute(**kwargs)
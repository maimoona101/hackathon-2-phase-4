"""
MCP Tool for completing tasks
This module implements the complete_task functionality for the AI agent
"""

import asyncio
from typing import Dict, Any
from sqlmodel import Session

from ...models.todo import Todo
from ...schemas.todo import TodoUpdate
from ...services.todo_service import TodoService


class CompleteTaskTool:
    def __init__(self, session: Session, user_id: str = None):
        self.session = session
        self.user_id = user_id
        self.service = TodoService(session)

    async def execute(self, task_id: str) -> Dict[str, Any]:
        """
        Execute the complete_task tool to mark a task as completed
        Maps to existing PATCH /api/todos/{task_id}/ endpoint functionality
        """
        try:
            # Validate required parameters
            if not task_id or not task_id.strip():
                raise ValueError("Task ID is required and cannot be empty")

            # Check if user_id is available
            if not self.user_id:
                raise ValueError("User context is required to complete a task")

            # Prepare the update data to mark as completed
            update_data = {
                'status': 'completed'
            }

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
            print(f"Successfully marked task '{updated_todo.title}' with ID {updated_todo.id} as completed")
            return result
        except ValueError as ve:
            # Handle validation errors
            error_msg = f"Validation error in complete_task: {str(ve)}"
            print(error_msg)
            raise ve
        except Exception as e:
            # Handle other errors
            error_msg = f"Error in complete_task tool: {str(e)}"
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
                "name": "complete_task",
                "description": "Mark a specific task as completed",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "string",
                            "description": "Unique identifier of the task to mark as completed"
                        }
                    },
                    "required": ["task_id"]
                }
            }
        }


# Async wrapper for easier use
async def run_complete_task(session: Session, user_id: str = None, task_id: str = None) -> Dict[str, Any]:
    tool = CompleteTaskTool(session, user_id)
    return await tool.execute(task_id)
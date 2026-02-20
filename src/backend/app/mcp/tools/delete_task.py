"""
MCP Tool for deleting tasks
This module implements the delete_task functionality for the AI agent
"""

import asyncio
from typing import Dict, Any
from sqlmodel import Session

from ...services.todo_service import TodoService


class DeleteTaskTool:
    def __init__(self, session: Session, user_id: str = None):
        self.session = session
        self.user_id = user_id
        self.service = TodoService(session)

    async def execute(self, task_id: str) -> Dict[str, Any]:
        """
        Execute the delete_task tool to remove a task
        Maps to existing DELETE /api/todos/{task_id}/ endpoint functionality
        """
        try:
            # Validate required parameters
            if not task_id or not task_id.strip():
                raise ValueError("Task ID is required and cannot be empty")

            # Check if user_id is available
            if not self.user_id:
                raise ValueError("User context is required to delete a task")

            # Use the existing TodoService to delete the task for the specific user
            success = self.service.delete_todo(task_id, self.user_id)

            if not success:
                raise ValueError(f"Task with ID {task_id} not found or not owned by user")

            # Return success message
            result = {
                "success": True,
                "message": f"Task with ID {task_id} deleted successfully"
            }

            # Log successful execution
            print(f"Successfully deleted task with ID {task_id}")
            return result
        except ValueError as ve:
            # Handle validation errors
            error_msg = f"Validation error in delete_task: {str(ve)}"
            print(error_msg)
            raise ve
        except Exception as e:
            # Handle other errors
            error_msg = f"Error in delete_task tool: {str(e)}"
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
                "name": "delete_task",
                "description": "Remove a task from the user's todo list",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "string",
                            "description": "Unique identifier of the task to delete"
                        }
                    },
                    "required": ["task_id"]
                }
            }
        }


# Async wrapper for easier use
async def run_delete_task(session: Session, user_id: str = None, task_id: str = None) -> Dict[str, Any]:
    tool = DeleteTaskTool(session, user_id)
    return await tool.execute(task_id)
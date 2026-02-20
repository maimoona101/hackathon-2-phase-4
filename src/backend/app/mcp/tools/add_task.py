"""
MCP Tool for adding tasks
This module implements the add_task functionality for the AI agent
"""

import asyncio
from typing import Dict, Any, Optional
from sqlmodel import Session

from ...models.todo import Todo
from ...schemas.todo import TodoCreate
from ...services.todo_service import TodoService


class AddTaskTool:
    def __init__(self, session: Session, user_id: str = None):
        self.session = session
        self.user_id = user_id
        self.service = TodoService(session)

    async def execute(self, title: str, description: Optional[str] = None, due_date: Optional[str] = None) -> Dict[str, Any]:
        """
        Execute the add_task tool to create a new task
        Maps to existing POST /api/todos/ endpoint functionality
        """
        try:
            # Validate required parameters
            if not title or not title.strip():
                raise ValueError("Title is required and cannot be empty")

            # Additional validation for due_date format if provided
            if due_date:
                from datetime import datetime
                try:
                    datetime.fromisoformat(due_date.replace('Z', '+00:00'))
                except ValueError:
                    raise ValueError(f"Invalid date format for due_date: {due_date}. Expected ISO format (YYYY-MM-DD)")

            # Check if user_id is available
            if not self.user_id:
                raise ValueError("User context is required to create a task")

            # Prepare the todo data
            todo_data = TodoCreate(
                title=title.strip(),
                description=description.strip() if description else None,
                due_date=due_date,
                status="pending"  # Default status for new tasks
            )

            # Use the existing TodoService to create the task for the specific user
            new_todo = self.service.create_todo(todo_data, self.user_id)

            # Return the created task in the expected format
            result = {
                "id": str(new_todo.id),
                "title": new_todo.title,
                "description": new_todo.description,
                "due_date": new_todo.due_date,
                "completed": new_todo.status == "completed",
                "created_at": new_todo.created_at.isoformat() if new_todo.created_at else None
            }

            # Log successful execution
            print(f"Successfully added task '{title}' with ID {new_todo.id}")
            return result
        except ValueError as ve:
            # Handle validation errors
            error_msg = f"Validation error in add_task: {str(ve)}"
            print(error_msg)
            raise ve
        except Exception as e:
            # Handle other errors
            error_msg = f"Error in add_task tool: {str(e)}"
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


# Async wrapper for easier use
async def run_add_task(session: Session, user_id: str = None, **kwargs) -> Dict[str, Any]:
    tool = AddTaskTool(session, user_id)
    return await tool.execute(**kwargs)
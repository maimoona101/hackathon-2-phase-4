"""
Gemini Agent for the Todo Chatbot
This module contains the AI agent configuration and initialization using Google Gemini
"""

import os
from typing import Dict, Any, List
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

class TodoAgent:
    def __init__(self):
        # Initialize the Gemini API with the key from environment
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set")

        genai.configure(api_key=api_key)

        # Initialize the generative model with the specified model
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            tools=self.get_available_functions()
        )

    def get_available_functions(self) -> List[Dict[str, Any]]:
        """
        Define the available functions/tools for the Gemini agent
        """
        return [
            {
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
            },
            {
                "name": "list_tasks",
                "description": "Retrieve the user's current todo list",
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
            },
            {
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
            },
            {
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
            },
            {
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
        ]

    def create_assistant(self):
        """Placeholder for Gemini - assistants concept is different in Gemini"""
        # In Gemini, we don't create assistants like in OpenAI
        # Instead, we use the model directly with tools
        return self.model

    def run_assistant(self, messages: list):
        """Run the Gemini model on the provided messages"""
        try:
            # Start a chat session and send the messages
            chat = self.model.start_chat(history=[])

            # Assuming the last message is the user input
            if messages:
                user_input = messages[-1]["content"] if isinstance(messages[-1], dict) else messages[-1]
                response = chat.send_message(user_input)
                return response
            else:
                raise ValueError("No messages provided")
        except Exception as e:
            print(f"Error running Gemini assistant: {str(e)}")
            raise e

# Global instance
todo_agent = TodoAgent()
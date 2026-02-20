"""
Gemini Agent for the Todo Chatbot
This module contains the AI agent configuration and initialization using Google Gemini
"""

import os
import json
from typing import Dict, Any, List
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

class GeminiTodoAgent:
    def __init__(self):
        # Initialize the Gemini API with the key from environment
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set")

        genai.configure(api_key=api_key)

        # Initialize the generative model with the specified model
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

        # Define tools for the model using Google's expected format
        self.tools = [
            {
                "function_declarations": [
                    {
                        "name": "add_task",
                        "description": "Create a new task in the user's todo list",
                        "parameters": {
                            "type": "OBJECT",
                            "properties": {
                                "title": {
                                    "type": "STRING",
                                    "description": "The title of the task"
                                },
                                "description": {
                                    "type": "STRING",
                                    "description": "Detailed description of the task"
                                },
                                "due_date": {
                                    "type": "STRING",
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
                            "type": "OBJECT",
                            "properties": {
                                "status": {
                                    "type": "STRING",
                                    "description": "Filter tasks by status: 'all', 'pending', 'completed'. Default: 'all'",
                                    "enum": ["all", "pending", "completed"]
                                },
                                "limit": {
                                    "type": "INTEGER",
                                    "description": "Maximum number of tasks to return. Default: 100"
                                },
                                "offset": {
                                    "type": "INTEGER",
                                    "description": "Number of tasks to skip for pagination. Default: 0"
                                }
                            }
                        }
                    },
                    {
                        "name": "update_task",
                        "description": "Modify an existing task in the user's todo list",
                        "parameters": {
                            "type": "OBJECT",
                            "properties": {
                                "task_id": {
                                    "type": "STRING",
                                    "description": "Unique identifier of the task to update"
                                },
                                "title": {
                                    "type": "STRING",
                                    "description": "New title for the task"
                                },
                                "description": {
                                    "type": "STRING",
                                    "description": "New description for the task"
                                },
                                "due_date": {
                                    "type": "STRING",
                                    "description": "New due date in YYYY-MM-DD format"
                                },
                                "completed": {
                                    "type": "BOOLEAN",
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
                            "type": "OBJECT",
                            "properties": {
                                "task_id": {
                                    "type": "STRING",
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
                            "type": "OBJECT",
                            "properties": {
                                "task_id": {
                                    "type": "STRING",
                                    "description": "Unique identifier of the task to delete"
                                }
                            },
                            "required": ["task_id"]
                        }
                    }
                ]
            }
        ]

        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            tools=self.tools
        )

    def run_gemini_conversation(self, messages: List[Dict[str, str]]):
        """
        Run a conversation with the Gemini model
        """
        try:
            # Convert messages to the format expected by Gemini
            chat = self.model.start_chat(history=[])

            # Send the user message and get response
            response = chat.send_message(
                messages[-1]["content"],  # Last message is typically the user input
                generation_config={
                    "temperature": 0.7,
                    "max_output_tokens": 2048,
                }
            )

            return response
        except Exception as e:
            print(f"Error in Gemini conversation: {str(e)}")
            raise e

# Global instance
gemini_todo_agent = GeminiTodoAgent()
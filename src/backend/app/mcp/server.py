"""
MCP Server Framework for the AI-powered Todo Chatbot
This module handles the execution of MCP tools and manages communication with the AI agent
"""

from typing import Dict, Any, Optional, Callable
from sqlmodel import Session
import asyncio
import json
from datetime import datetime

from .tools.add_task import AddTaskTool, run_add_task
from .tools.list_tasks import ListTasksTool, run_list_tasks
from .tools.update_task import UpdateTaskTool, run_update_task
from .tools.complete_task import CompleteTaskTool, run_complete_task
from .tools.delete_task import DeleteTaskTool, run_delete_task


class MCPServer:
    def __init__(self):
        self.tools = {}
        self.register_default_tools()

    def register_tool(self, name: str, executor: Callable):
        """
        Register a tool with the MCP server
        """
        self.tools[name] = executor
        print(f"Registered tool: {name}")

    def register_default_tools(self):
        """
        Register all the default todo management tools
        """
        self.register_tool("add_task", run_add_task)
        self.register_tool("list_tasks", run_list_tasks)
        self.register_tool("update_task", run_update_task)
        self.register_tool("complete_task", run_complete_task)
        self.register_tool("delete_task", run_delete_task)

    async def execute_tool(self, tool_name: str, session: Session, user_id: str = None, **params) -> Dict[str, Any]:
        """
        Execute a tool with the given parameters
        """
        if tool_name not in self.tools:
            raise ValueError(f"Unknown tool: {tool_name}")

        # Execute the tool with the provided parameters
        try:
            result = await self.tools[tool_name](session, user_id, **params)
            return {
                "success": True,
                "result": result,
                "execution_time": datetime.utcnow().isoformat()
            }
        except Exception as e:
            # Log the error
            error_msg = str(e)
            print(f"Error executing tool {tool_name}: {error_msg}")

            return {
                "success": False,
                "error": error_msg,
                "execution_time": datetime.utcnow().isoformat()
            }

    def get_tool_definitions(self) -> list:
        """
        Get definitions for all registered tools
        This is used for registering tools with the OpenAI agent
        """
        # This would return the function definitions for each tool
        # Since each tool class has a get_tool_definition method, we'd need to instantiate them
        # For now, we'll return a placeholder that indicates which tools are available
        return [
            AddTaskTool(None).get_tool_definition(),
            ListTasksTool(None).get_tool_definition(),
            UpdateTaskTool(None).get_tool_definition(),
            CompleteTaskTool(None).get_tool_definition(),
            DeleteTaskTool(None).get_tool_definition()
        ]

    def validate_tool_call(self, tool_call: Dict[str, Any]) -> bool:
        """
        Validate a tool call before execution
        """
        if "name" not in tool_call or "arguments" not in tool_call:
            return False

        tool_name = tool_call["name"]
        arguments = tool_call["arguments"]

        # Check if tool exists
        if tool_name not in self.tools:
            return False

        # Additional validation can be added here based on tool requirements
        return True


# Global instance
mcp_server = MCPServer()
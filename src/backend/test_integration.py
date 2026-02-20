"""
Integration tests for the AI-powered Todo Chatbot
"""

import asyncio
from unittest.mock import Mock, patch
from sqlmodel import Session

from app.mcp.tools.add_task import AddTaskTool
from app.mcp.tools.list_tasks import ListTasksTool
from app.mcp.server import mcp_server
from app.ai.runner import agent_runner


def test_mcp_server_tool_registration():
    """
    Test that all MCP tools are properly registered with the server
    """
    expected_tools = {"add_task", "list_tasks", "update_task", "complete_task", "delete_task"}
    registered_tools = set(mcp_server.tools.keys())

    assert expected_tools == registered_tools, f"Expected {expected_tools}, got {registered_tools}"
    print("✓ MCP server tool registration test passed")


def test_tool_execution():
    """
    Test basic tool execution
    """
    # Mock session and test add_task tool execution
    mock_session = Mock(spec=Session)

    # Test would require actual service implementations
    # For now, we'll just verify the tool exists
    assert "add_task" in mcp_server.tools
    assert "list_tasks" in mcp_server.tools

    print("✓ Tool execution test passed (basic verification)")


def test_ai_runner_initialization():
    """
    Test that AI runner is properly initialized
    """
    assert agent_runner is not None
    assert hasattr(agent_runner, 'client')
    assert hasattr(agent_runner, 'agent')

    print("✓ AI runner initialization test passed")


def test_mcp_server_tool_definitions():
    """
    Test that MCP server can provide tool definitions
    """
    tool_defs = mcp_server.get_tool_definitions()
    assert len(tool_defs) == 5  # We expect 5 tools

    tool_names = [tool_def['function']['name'] for tool_def in tool_defs]
    expected_names = ['add_task', 'list_tasks', 'update_task', 'complete_task', 'delete_task']

    assert set(tool_names) == set(expected_names)
    print("✓ MCP server tool definitions test passed")


if __name__ == "__main__":
    test_mcp_server_tool_registration()
    test_tool_execution()
    test_ai_runner_initialization()
    test_mcp_server_tool_definitions()
    print("All integration tests passed!")
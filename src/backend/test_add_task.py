"""
Test file for the add_task MCP tool
"""

import asyncio
from unittest.mock import Mock, MagicMock
from sqlmodel import Session

from app.mcp.tools.add_task import AddTaskTool, run_add_task


def test_add_task_basic():
    """
    Test basic functionality of add_task tool
    """
    # Mock the session and service
    mock_session = Mock(spec=Session)

    # Mock the TodoService and its create_todo method
    from app.services.todo_service import TodoService
    mock_service = Mock(spec=TodoService)
    mock_todo = Mock()
    mock_todo.id = "12345"
    mock_todo.title = "Test task"
    mock_todo.description = "Test description"
    mock_todo.due_date = "2023-12-31"
    mock_todo.status = "pending"
    from datetime import datetime
    mock_todo.created_at = datetime.now()

    mock_service.create_todo.return_value = mock_todo

    # Patch the TodoService constructor to return our mock
    import app.mcp.tools.add_task
    original_todo_service_init = app.mcp.tools.add_task.TodoService.__init__
    app.mcp.tools.add_task.TodoService.__init__ = lambda self, session: None
    app.mcp.tools.add_task.TodoService.create_todo = mock_service.create_todo

    try:
        # Create the tool
        tool = AddTaskTool(mock_session, user_id="user123")

        # Execute the tool
        result = asyncio.run(
            tool.execute(title="Test task", description="Test description", due_date="2023-12-31")
        )

        # Verify the result
        assert result["id"] == "12345"
        assert result["title"] == "Test task"
        assert result["description"] == "Test description"
        assert result["due_date"] == "2023-12-31"
        assert result["completed"] is False

        print("✓ Basic add_task test passed")

        # Test with minimal parameters
        result_minimal = asyncio.run(
            tool.execute(title="Minimal task")
        )

        assert result_minimal["title"] == "Minimal task"
        assert result_minimal["description"] is None

        print("✓ Minimal parameters test passed")

        # Test validation error for empty title
        try:
            asyncio.run(tool.execute(title=""))
            assert False, "Expected ValueError for empty title"
        except ValueError as e:
            assert "Title is required" in str(e)
            print("✓ Empty title validation test passed")

    finally:
        # Restore original TodoService
        app.mcp.tools.add_task.TodoService.__init__ = original_todo_service_init


if __name__ == "__main__":
    test_add_task_basic()
    print("All add_task tests passed!")
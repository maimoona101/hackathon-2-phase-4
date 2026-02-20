"""
Test file for the list_tasks MCP tool
"""

import asyncio
from unittest.mock import Mock
from sqlmodel import Session
from datetime import datetime

from app.mcp.tools.list_tasks import ListTasksTool, run_list_tasks


def test_list_tasks_basic():
    """
    Test basic functionality of list_tasks tool
    """
    # Mock the session and service
    mock_session = Mock(spec=Session)

    # Mock the TodoService and its get_todos_by_user method
    from app.services.todo_service import TodoService
    mock_service = Mock(spec=TodoService)

    # Create mock todo objects
    mock_todo1 = Mock()
    mock_todo1.id = "12345"
    mock_todo1.title = "Test task 1"
    mock_todo1.description = "Test description 1"
    mock_todo1.due_date = "2023-12-31"
    mock_todo1.status = "pending"
    mock_todo1.created_at = datetime.now()

    mock_todo2 = Mock()
    mock_todo2.id = "67890"
    mock_todo2.title = "Test task 2"
    mock_todo2.description = "Test description 2"
    mock_todo2.due_date = "2024-01-15"
    mock_todo2.status = "completed"
    mock_todo2.created_at = datetime.now()

    mock_service.get_todos_by_user.return_value = [mock_todo1, mock_todo2]

    # Patch the TodoService constructor to return our mock
    import app.mcp.tools.list_tasks
    original_todo_service_init = app.mcp.tools.list_tasks.TodoService.__init__
    app.mcp.tools.list_tasks.TodoService.__init__ = lambda self, session: None
    app.mcp.tools.list_tasks.TodoService.get_todos_by_user = mock_service.get_todos_by_user

    try:
        # Create the tool
        tool = ListTasksTool(mock_session, user_id="user123")

        # Execute the tool
        result = asyncio.run(
            tool.execute(status="all", limit=10, offset=0)
        )

        # Verify the result
        assert len(result) == 2
        assert result[0]["id"] == "12345"
        assert result[0]["title"] == "Test task 1"
        assert result[0]["completed"] is False  # pending status
        assert result[1]["id"] == "67890"
        assert result[1]["title"] == "Test task 2"
        assert result[1]["completed"] is True  # completed status

        print("✓ Basic list_tasks test passed")

        # Test with different status
        result_pending = asyncio.run(
            tool.execute(status="pending")
        )

        assert len(result_pending) == 2  # Our mock returns the same regardless of status filter

        print("✓ Different status test passed")

        # Test validation error for invalid status
        try:
            asyncio.run(tool.execute(status="invalid"))
            assert False, "Expected ValueError for invalid status"
        except ValueError as e:
            assert "Invalid status" in str(e)
            print("✓ Invalid status validation test passed")

    finally:
        # Restore original TodoService
        app.mcp.tools.list_tasks.TodoService.__init__ = original_todo_service_init


if __name__ == "__main__":
    test_list_tasks_basic()
    print("All list_tasks tests passed!")
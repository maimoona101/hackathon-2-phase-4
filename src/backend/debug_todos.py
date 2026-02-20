#!/usr/bin/env python3
"""
Debug script to test the todos endpoint functionality
"""
import time
from sqlmodel import Session, select
from app.database.session import get_session, SessionLocal
from app.models.todo import Todo
from app.services.todo_service import TodoService

def test_get_todos():
    print("Starting test of get_todos functionality...")

    # Create session using the same approach as the API
    session = next(get_session())

    try:
        print("Session created, testing query...")

        # Test the raw query
        start_time = time.time()
        query = select(Todo).where(Todo.user_id == "b9c18659-91ca-4628-b797-179f8c8ef171")  # Our test user ID
        result = session.execute(query)
        todos = result.scalars().all()
        end_time = time.time()

        print(f"Raw query executed in {end_time - start_time:.2f} seconds")
        print(f"Found {len(todos)} todos")

        # Test the service method
        service = TodoService(session)
        start_time = time.time()
        todos_from_service = service.get_todos_by_user(user_id="b9c18659-91ca-4628-b797-179f8c8ef171")
        end_time = time.time()

        print(f"Service method executed in {end_time - start_time:.2f} seconds")
        print(f"Found {len(todos_from_service)} todos via service")

    except Exception as e:
        print(f"Error occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        session.close()

if __name__ == "__main__":
    test_get_todos()
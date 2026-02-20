#!/usr/bin/env python3
"""
Test script to verify the update functionality
"""
from sqlmodel import Session, select
from app.database.session import get_session
from app.models.todo import Todo
from app.schemas.todo import TodoUpdate
from app.services.todo_service import TodoService

def test_update_functionality():
    print("Testing update functionality...")

    # Create session
    session = next(get_session())

    try:
        # Find a todo to update
        result = session.execute(select(Todo))
        todos = result.scalars().all()
        print(f"Found {len(todos)} todos")

        if todos:
            todo_to_update = todos[0]  # Take the first todo
            print(f"Updating todo with ID: {todo_to_update.id}, user_id: {todo_to_update.user_id}")

            # Create update object
            update_data = TodoUpdate(completed=True, title="Updated Title")

            # Create service and update
            service = TodoService(session)
            updated_todo = service.update_todo(str(todo_to_update.id), update_data, str(todo_to_update.user_id))

            if updated_todo:
                print(f"Successfully updated todo! New title: {updated_todo.title}, Completed: {updated_todo.completed}")
            else:
                print("Failed to update todo - might be due to user mismatch")
        else:
            # Create a test todo if none exist
            print("Creating a test todo first...")
            from app.models.user import User
            from app.schemas.todo import TodoCreate

            # Get an existing user to associate with the todo
            user_result = session.execute(select(User))
            users = user_result.scalars().all()

            if users:
                test_user = users[0]
                test_todo = Todo(title="Test Todo", completed=False, user_id=test_user.id)
                session.add(test_todo)
                session.commit()
                session.refresh(test_todo)

                print(f"Created test todo with ID: {test_todo.id}")

                # Now try to update it
                update_data = TodoUpdate(completed=True, title="Updated Title")
                service = TodoService(session)
                updated_todo = service.update_todo(str(test_todo.id), update_data, str(test_todo.user_id))

                if updated_todo:
                    print(f"Successfully updated todo! New title: {updated_todo.title}, Completed: {updated_todo.completed}")
                else:
                    print("Failed to update newly created todo")
            else:
                print("No users found to create a test todo")
    except Exception as e:
        print(f"Error occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        session.close()

if __name__ == "__main__":
    test_update_functionality()
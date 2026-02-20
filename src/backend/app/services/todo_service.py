from typing import List, Optional
from sqlmodel import Session, select
from ..models.todo import Todo, TodoBase
from ..models.user import User
from ..schemas.todo import TodoCreate, TodoUpdate


class TodoService:
    def __init__(self, session: Session):
        self.session = session

    def create_todo(self, todo_data: TodoCreate, user_id: str) -> Todo:
        """Create a new todo for the specified user"""
        todo = Todo(
            title=todo_data.title,
            completed=todo_data.completed,
            user_id=user_id
        )
        self.session.add(todo)
        self.session.commit()
        self.session.refresh(todo)
        return todo

    def get_todo_by_id(self, todo_id: str, user_id: str) -> Optional[Todo]:
        """Get a specific todo by ID for the specified user"""
        todo = self.session.get(Todo, todo_id)
        if todo and str(todo.user_id) == user_id:
            return todo
        return None

    def get_todos_by_user(
        self,
        user_id: str,
        completed: Optional[bool] = None,
        limit: int = 50,
        offset: int = 0,
        sort_by: str = "created_at",
        sort_order: str = "desc"
    ) -> List[Todo]:
        """Get all todos for the specified user with optional filters"""
        query = select(Todo).where(Todo.user_id == user_id)

        if completed is not None:
            query = query.where(Todo.completed == completed)

        # Add sorting
        if sort_by == "created_at":
            if sort_order == "asc":
                query = query.order_by(Todo.created_at)
            else:
                query = query.order_by(Todo.created_at.desc())

        # Apply limit and offset
        query = query.offset(offset).limit(limit)

        # Execute the query and return the results
        statement_result = self.session.execute(query)
        todos = statement_result.scalars().all()
        return todos

    def update_todo(self, todo_id: str, todo_update: TodoUpdate, user_id: str) -> Optional[Todo]:
        """Update a specific todo for the specified user"""
        todo = self.get_todo_by_id(todo_id, user_id)
        if todo:
            update_data = todo_update.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(todo, field, value)

            self.session.add(todo)
            self.session.commit()
            self.session.refresh(todo)
            return todo
        return None

    def delete_todo(self, todo_id: str, user_id: str) -> bool:
        """Delete a specific todo for the specified user"""
        todo = self.get_todo_by_id(todo_id, user_id)
        if todo:
            self.session.delete(todo)
            self.session.commit()
            return True
        return False
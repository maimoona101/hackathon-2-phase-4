from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from typing import List, Optional
from ...database.session import get_session
from ...models.todo import Todo
from ...schemas.todo import TodoCreate, TodoRead, TodoUpdate
from ...api.deps import get_current_user
from ...models.user import User
from ...services.todo_service import TodoService


router = APIRouter()


@router.get("/", response_model=List[TodoRead])
def get_todos(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    completed: Optional[bool] = Query(None, description="Filter by completion status: true for completed, false for pending"),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of todos to return"),
    offset: int = Query(0, ge=0, description="Number of todos to skip"),
    sort_by: str = Query("created_at", description="Field to sort by"),
    sort_order: str = Query("desc", description="Sort order: asc or desc")
):
    """
    Get all todos for the authenticated user with optional filtering and pagination
    """
    service = TodoService(session)
    todos = service.get_todos_by_user(
        user_id=str(current_user.id),
        completed=completed,
        limit=limit,
        offset=offset,
        sort_by=sort_by,
        sort_order=sort_order
    )
    return todos


@router.post("/", response_model=TodoRead)
def create_todo(
    todo_data: TodoCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new todo for the authenticated user
    """
    service = TodoService(session)
    todo = service.create_todo(todo_data, str(current_user.id))
    return todo


@router.get("/{todo_id}", response_model=TodoRead)
def get_todo(
    todo_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get a specific todo by ID for the authenticated user
    """
    service = TodoService(session)
    todo = service.get_todo_by_id(todo_id, str(current_user.id))
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    return todo


@router.put("/{todo_id}", response_model=TodoRead)
def update_todo(
    todo_id: str,
    todo_update: TodoUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update a specific todo for the authenticated user
    """
    service = TodoService(session)
    todo = service.update_todo(todo_id, todo_update, str(current_user.id))
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    return todo


@router.delete("/{todo_id}")
def delete_todo(
    todo_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a specific todo for the authenticated user
    """
    service = TodoService(session)
    success = service.delete_todo(todo_id, str(current_user.id))
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    return {"message": "Todo deleted successfully"}
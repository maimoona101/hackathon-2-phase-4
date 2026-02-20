from fastapi import APIRouter, Depends
from sqlmodel import Session
from ...database.session import get_session
from ...models.user import User
from ...schemas.user import UserRead
from ...api.deps import get_current_user


router = APIRouter()


@router.get("/profile", response_model=UserRead)
def get_profile(current_user: User = Depends(get_current_user)):
    """
    Get current user's profile
    """
    return current_user


@router.put("/profile", response_model=UserRead)
def update_profile(
    display_name: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update current user's profile
    """
    current_user.display_name = display_name
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return current_user
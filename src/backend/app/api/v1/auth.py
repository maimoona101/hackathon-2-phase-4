from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from pydantic import BaseModel

from ...database.session import get_session
from ...models.user import User
from ...schemas.user import UserCreate, UserRead
from ...schemas.auth import Token
from ...auth.security import get_password_hash, verify_password
from ...auth.jwt_handler import create_access_token

router = APIRouter()


class LoginData(BaseModel):
    email: str
    password: str

@router.post("/register", response_model=UserRead)
def register(user_data: UserCreate, session: Session = Depends(get_session)):
    user = session.execute(
        select(User).where(User.email == user_data.email)
    ).scalar_one_or_none()

    if user:
        raise HTTPException(status_code=409, detail="Email already registered")

    new_user = User(
        email=user_data.email,
        display_name=user_data.display_name,
        hashed_password=get_password_hash(user_data.password)
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user


@router.post("/login", response_model=Token)
def login(login_data: LoginData, session: Session = Depends(get_session)):
    try:
        # Query for the user
        user_result = session.execute(
            select(User).where(User.email == login_data.email)
        )
        user = user_result.scalar_one_or_none()

        if not user or not verify_password(login_data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Incorrect email or password")

        access_token = create_access_token(
            data={"sub": str(user.id)},
            expires_delta=timedelta(minutes=30)
        )

        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Log the actual error for debugging
        print(f"Login error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal server error during login")

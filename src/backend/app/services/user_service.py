from typing import Optional
from sqlmodel import Session, select
from ..models.user import User
from ..schemas.user import UserCreate
from ..auth.security import get_password_hash


class UserService:
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, user_data: UserCreate) -> User:
        """Create a new user"""
        # Hash the password before storing
        hashed_password = get_password_hash(user_data.password)
        user = User(
            email=user_data.email,
            password_hash=hashed_password,
            display_name=user_data.display_name
        )
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get a user by email"""
        statement = select(User).where(User.email == email)
        return self.session.execute(statement).first()

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get a user by ID"""
        return self.session.get(User, user_id)
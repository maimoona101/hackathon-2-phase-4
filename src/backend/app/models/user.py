from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
import uuid
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .todo import Todo
    from .conversation import Conversation
    from .user_session import UserSession


class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False)
    display_name: str | None = Field(default=None)


class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to todos
    todos: Optional[list["Todo"]] = Relationship(back_populates="user")

    # Relationships for AI chatbot
    conversations: Optional[list["Conversation"]] = Relationship(back_populates="user")
    sessions: Optional[list["UserSession"]] = Relationship(back_populates="user")
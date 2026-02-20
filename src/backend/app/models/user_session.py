"""
UserSession model for the AI-powered Todo Chatbot
"""

from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import TYPE_CHECKING
import uuid

if TYPE_CHECKING:
    from .user import User


class UserSessionBase(SQLModel):
    user_id: uuid.UUID = Field(foreign_key="user.id")
    session_token: str
    expires_at: datetime


class UserSession(UserSessionBase, table=True):
    __tablename__ = "user_sessions"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    user: "User" = Relationship(back_populates="sessions")


class UserSessionRead(UserSessionBase):
    id: str
    created_at: datetime


# Pydantic schemas for creation and update
from pydantic import BaseModel
from datetime import datetime


class UserSessionCreate(BaseModel):
    user_id: str  # Using str to accept UUID string
    session_token: str
    expires_at: datetime
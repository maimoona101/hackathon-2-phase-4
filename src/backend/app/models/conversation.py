"""
Conversation model for the AI-powered Todo Chatbot
"""

from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, TYPE_CHECKING
import uuid
from sqlalchemy import Column, JSON

# Use TYPE_CHECKING to avoid circular imports
if TYPE_CHECKING:
    from .user import User
    from .message import Message


# Base class for shared fields
class ConversationBase(SQLModel):
    user_id: uuid.UUID = Field(foreign_key="user.id")
    metadata_json: Optional[dict] = Field(default=None, sa_column=Column(JSON, name="metadata"))


# Main Conversation table
class Conversation(ConversationBase, table=True):
    __tablename__ = "conversations"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: "User" = Relationship(back_populates="conversations")
    messages: Optional[list["Message"]] = Relationship(back_populates="conversation")


# Read schema
class ConversationRead(ConversationBase):
    id: str
    created_at: datetime
    updated_at: datetime


# Pydantic schemas for creation and update
class ConversationCreate(SQLModel):
    user_id: uuid.UUID
    metadata_json: Optional[dict] = None


class ConversationUpdate(SQLModel):
    metadata_json: Optional[dict] = None

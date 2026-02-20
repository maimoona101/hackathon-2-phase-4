"""
Message model for the AI-powered Todo Chatbot
"""

from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, TYPE_CHECKING
import uuid
from sqlalchemy import Column, JSON

# Avoid circular import
if TYPE_CHECKING:
    from .conversation import Conversation


class MessageBase(SQLModel):
    conversation_id: str = Field(foreign_key="conversations.id")
    role: str = Field(regex="^(user|assistant|tool)$")  # user, assistant, or tool
    content: str
    tool_calls: Optional[list] = Field(default=None, sa_column=Column(JSON))
    tool_responses: Optional[list] = Field(default=None, sa_column=Column(JSON))


class Message(MessageBase, table=True):
    __tablename__ = "messages"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    conversation: "Conversation" = Relationship(back_populates="messages")


# Pydantic read schema
class MessageRead(MessageBase):
    id: str
    timestamp: datetime

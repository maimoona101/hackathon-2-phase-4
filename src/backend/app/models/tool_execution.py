"""
ToolExecution model for the AI-powered Todo Chatbot
"""

from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import TYPE_CHECKING, Optional
import uuid
from sqlalchemy import Column, JSON

if TYPE_CHECKING:
    from .conversation import Conversation


class ToolExecutionBase(SQLModel):
    conversation_id: str = Field(foreign_key="conversations.id")
    tool_name: str = Field(regex="^(add_task|list_tasks|update_task|complete_task|delete_task)$")
    parameters: dict = Field(sa_column=Column(JSON))
    result: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    success: bool = Field(default=True)


class ToolExecution(ToolExecutionBase, table=True):
    __tablename__ = "tool_executions"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    execution_time: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    conversation: "Conversation" = Relationship()


class ToolExecutionRead(ToolExecutionBase):
    id: str
    execution_time: datetime
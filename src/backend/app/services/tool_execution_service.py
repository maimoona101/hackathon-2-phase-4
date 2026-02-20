"""
ToolExecution Service for the AI-powered Todo Chatbot
"""

from sqlmodel import Session, select
from typing import Optional, List
from datetime import datetime
import uuid

from ..models.tool_execution import ToolExecution, ToolExecutionCreate


class ToolExecutionService:
    def __init__(self, session: Session):
        self.session = session

    def create_tool_execution(self, conversation_id: str, tool_name: str, parameters: dict, result: dict = None, success: bool = True) -> ToolExecution:
        """Create a new tool execution record"""
        tool_execution = ToolExecution(
            conversation_id=conversation_id,
            tool_name=tool_name,
            parameters=parameters,
            result=result,
            success=success
        )
        self.session.add(tool_execution)
        self.session.commit()
        self.session.refresh(tool_execution)
        return tool_execution

    def get_tool_execution_by_id(self, tool_execution_id: str) -> Optional[ToolExecution]:
        """Get a specific tool execution by ID"""
        statement = select(ToolExecution).where(ToolExecution.id == tool_execution_id)
        return self.session.exec(statement).first()

    def get_tool_executions_by_conversation(self, conversation_id: str) -> List[ToolExecution]:
        """Get all tool executions for a conversation"""
        statement = select(ToolExecution).where(ToolExecution.conversation_id == conversation_id)
        return self.session.exec(statement).all()

    def get_tool_executions_by_tool_name(self, tool_name: str) -> List[ToolExecution]:
        """Get all tool executions for a specific tool"""
        statement = select(ToolExecution).where(ToolExecution.tool_name == tool_name)
        return self.session.exec(statement).all()


# Create a temporary schema for the service until we create the proper ones
from pydantic import BaseModel

class ToolExecutionCreate(BaseModel):
    conversation_id: str
    tool_name: str
    parameters: dict
    result: Optional[dict] = None
    success: bool = True
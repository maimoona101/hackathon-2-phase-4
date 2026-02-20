"""
Schema definitions for the AI chatbot functionality
"""

from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class ChatRequest(BaseModel):
    """
    Request schema for chat messages
    """
    conversation_id: Optional[str] = None
    message: str
    user_token: Optional[str] = None


class ChatResponse(BaseModel):
    """
    Response schema for chat messages
    """
    response: str
    conversation_id: str
    tool_calls: Optional[list] = None
    timestamp: datetime = datetime.now()
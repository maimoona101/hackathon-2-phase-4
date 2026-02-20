"""
Chat API router for the AI-powered Todo Chatbot
This module contains endpoints for managing AI chat conversations
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional
from sqlmodel import Session
import uuid
from datetime import datetime

from ...database.session import get_session
from ...api.deps import get_current_user
from ...models.user import User
from ...schemas.chat import ChatRequest, ChatResponse
from ...mcp.server import mcp_server
from ...ai.runner import agent_runner
from ...services.conversation_service import ConversationService
from ...services.session_service import SessionService


router = APIRouter()


@router.post("/start", response_model=dict)
async def start_conversation(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Start a new chat conversation for the authenticated user
    """
    try:
        # Create a conversation using the conversation service
        conversation_service = ConversationService(session)
        conversation = conversation_service.create_conversation(current_user.id)

        return {
            "conversation_id": conversation.id,
            "message": "Conversation started successfully",
            "timestamp": conversation.created_at.isoformat()
        }
    except Exception as e:
        print(f"Error starting conversation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to start conversation"
        )


@router.post("/message", response_model=ChatResponse)
async def send_message(
    chat_request: ChatRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Send a message to the AI chatbot and receive a response
    """
    try:
        # If no conversation_id provided, start a new conversation
        conversation_id = chat_request.conversation_id
        if not conversation_id:
            conversation_service = ConversationService(session)
            conversation = conversation_service.create_conversation(current_user.id)
            conversation_id = conversation.id

        # Process the conversation using the AI agent
        # This connects to the Gemini agent to process the message
        result = await agent_runner.process_conversation(
            user_message=chat_request.message,
            session=session,
            user_id=str(current_user.id)
        )

        # Use the actual response from the AI agent
        response_text = result.get("response", f"Processed your message: '{chat_request.message}'")

        return ChatResponse(
            response=response_text,
            conversation_id=conversation_id
        )
    except Exception as e:
        print(f"Error processing message: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process message"
        )


@router.get("/history/{conversation_id}", response_model=list)
async def get_conversation_history(
    conversation_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Retrieve the history of a specific conversation
    """
    try:
        # Verify that the conversation belongs to the current user
        conversation_service = ConversationService(session)
        conversation = conversation_service.get_conversation_by_id(conversation_id, current_user.id)

        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )

        # In a full implementation, we would return the actual message history
        # For now, return a placeholder
        return [{"role": "assistant", "content": "Conversation history will be implemented in future iterations"}]
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error retrieving conversation history: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve conversation history"
        )
"""
Conversation Service for the AI-powered Todo Chatbot
"""

from sqlmodel import Session, select
from typing import Optional
from datetime import datetime
import uuid

from ..models.conversation import Conversation, ConversationCreate, ConversationUpdate
from ..models.user import User


class ConversationService:
    def __init__(self, session: Session):
        self.session = session

    def create_conversation(self, user_id: int) -> Conversation:
        """Create a new conversation for a user"""
        conversation = Conversation(user_id=user_id)
        self.session.add(conversation)
        self.session.commit()
        self.session.refresh(conversation)
        return conversation

    def get_conversation_by_id(self, conversation_id: str, user_id: int) -> Optional[Conversation]:
        """Get a specific conversation by ID for a user"""
        statement = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        return self.session.exec(statement).first()

    def get_conversations_by_user(self, user_id: int) -> list[Conversation]:
        """Get all conversations for a user"""
        statement = select(Conversation).where(Conversation.user_id == user_id)
        return self.session.exec(statement).all()

    def update_conversation(self, conversation_id: str, user_id: int, updates: dict) -> Optional[Conversation]:
        """Update a conversation"""
        conversation = self.get_conversation_by_id(conversation_id, user_id)
        if conversation:
            for key, value in updates.items():
                setattr(conversation, key, value)
            conversation.updated_at = datetime.utcnow()
            self.session.add(conversation)
            self.session.commit()
            self.session.refresh(conversation)
        return conversation

    def delete_conversation(self, conversation_id: str, user_id: int) -> bool:
        """Delete a conversation"""
        conversation = self.get_conversation_by_id(conversation_id, user_id)
        if conversation:
            self.session.delete(conversation)
            self.session.commit()
            return True
        return False